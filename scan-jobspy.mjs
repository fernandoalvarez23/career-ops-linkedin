#!/usr/bin/env node
/**
 * scan-jobspy.mjs
 * Scraper de LinkedIn + Indeed via JobSpy (Python) para career-ops.
 *
 * Requiere: /opt/homebrew/bin/python3.11 con python-jobspy instalado
 *   /opt/homebrew/bin/python3.11 -m pip install python-jobspy
 *
 * Uso:
 *   node scan-jobspy.mjs --market ar           # busca en Argentina
 *   node scan-jobspy.mjs --market es           # busca en España
 *   node scan-jobspy.mjs --market both         # ambos mercados
 *   node scan-jobspy.mjs --market ar --dry-run # preview sin escribir
 *   node scan-jobspy.mjs --market ar --hours 48 --results 30
 *
 * ⚠️  AVISO LEGAL: LinkedIn e Indeed prohíben scraping en sus ToS.
 *    Este script es para uso personal en búsqueda de empleo propia.
 *    No usar para fines comerciales ni scraping masivo.
 */

import { execFileSync } from 'child_process';
import { readFileSync, writeFileSync, existsSync, appendFileSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';
import yaml from 'js-yaml';

const __dirname = dirname(fileURLToPath(import.meta.url));
const PYTHON = '/opt/homebrew/bin/python3.11';

// --- Parse args ---
const args = process.argv.slice(2);
const getArg = (flag, def) => {
  const i = args.indexOf(flag);
  return i !== -1 && args[i + 1] ? args[i + 1] : def;
};
const hasFlag = (flag) => args.includes(flag);

const market = getArg('--market', 'ar').toLowerCase();
const dryRun = hasFlag('--dry-run');
const hoursOld = parseInt(getArg('--hours', '72'));
const resultsWanted = parseInt(getArg('--results', '50'));
const sites = getArg('--sites', 'linkedin,indeed').split(',');

if (!['ar', 'es', 'both'].includes(market)) {
  console.error('❌  --market debe ser: ar | es | both');
  process.exit(1);
}

// --- Load config ---
const profilePath = join(__dirname, 'config/profile.yml');
const portalsPath = join(__dirname, 'portals.yml');

if (!existsSync(profilePath)) {
  console.error('❌  config/profile.yml no encontrado. Completá tu perfil primero.');
  process.exit(1);
}

const profile = yaml.load(readFileSync(profilePath, 'utf8'));
const portals = existsSync(portalsPath) ? yaml.load(readFileSync(portalsPath, 'utf8')) : null;

// Search terms from profile
const primaryRoles = profile?.target_roles?.primary ?? ['Product Manager', 'Project Manager'];
const titleFilter = portals?.title_filter ?? { positive: ['Product Manager'], negative: ['Junior'] };

// Market configs
const marketConfigs = {
  ar: [
    { location: 'Argentina', country_indeed: 'Argentina', label: 'AR' },
    { location: 'Buenos Aires', country_indeed: 'Argentina', label: 'AR-BUE' },
  ],
  es: [
    { location: 'Madrid, Spain', country_indeed: 'Spain', label: 'ES-MAD' },
    { location: 'Barcelona, Spain', country_indeed: 'Spain', label: 'ES-BCN' },
    { location: 'Spain remote', country_indeed: 'Spain', label: 'ES-REMOTE' },
  ],
};

const targetsToScan = market === 'both'
  ? [...marketConfigs.ar, ...marketConfigs.es]
  : marketConfigs[market] ?? marketConfigs.ar;

// --- Dedup helpers ---
const historyPath = join(__dirname, 'data/scan-history.tsv');
const pipelinePath = join(__dirname, 'data/pipeline.md');

const loadHistory = () => {
  if (!existsSync(historyPath)) return new Set();
  return new Set(
    readFileSync(historyPath, 'utf8')
      .split('\n')
      .filter(Boolean)
      .map(l => l.split('\t')[0])
  );
};

const loadPipelineUrls = () => {
  if (!existsSync(pipelinePath)) return new Set();
  const urls = new Set();
  for (const line of readFileSync(pipelinePath, 'utf8').split('\n')) {
    const m = line.match(/https?:\/\/\S+/);
    if (m) urls.add(m[0].replace(/[)>].*$/, '').trim());
  }
  return urls;
};

// --- Title filter ---
const matchesFilter = (title) => {
  if (!title) return false;
  const t = title.toLowerCase();
  const hasPositive = titleFilter.positive.some(kw => t.includes(kw.toLowerCase()));
  const hasNegative = titleFilter.negative.some(kw => t.includes(kw.toLowerCase()));
  return hasPositive && !hasNegative;
};

// --- Python script (inline) ---
const buildPythonScript = (searchTerm, location, countryIndeed) => `
import json, sys
from jobspy import scrape_jobs

try:
    jobs = scrape_jobs(
        site_name=${JSON.stringify(sites)},
        search_term=${JSON.stringify(searchTerm)},
        location=${JSON.stringify(location)},
        results_wanted=${resultsWanted},
        hours_old=${hoursOld},
        country_indeed=${JSON.stringify(countryIndeed)},
        linkedin_fetch_description=False,
        verbose=0
    )
    if jobs is None or len(jobs) == 0:
        print("[]")
    else:
        cols = [c for c in ["title","company","location","job_url","date_posted","min_amount","max_amount","currency","job_type"] if c in jobs.columns]
        print(jobs[cols].to_json(orient="records", date_format="iso"))
except Exception as e:
    print(json.dumps({"error": str(e)}), file=sys.stderr)
    print("[]")
`;

// --- Main ---
async function runScan() {
  console.log(`\n🔍  scan-jobspy | market: ${market.toUpperCase()} | sites: ${sites.join(',')} | últimas ${hoursOld}h`);
  if (dryRun) console.log('   [dry-run — no se escribe nada]\n');

  const seenUrls = new Set([...loadHistory(), ...loadPipelineUrls()]);
  const newJobs = [];

  for (const { location, country_indeed, label } of targetsToScan) {
    for (const searchTerm of primaryRoles) {
      console.log(`   🌐  [${label}] "${searchTerm}" en "${location}"...`);

      const script = buildPythonScript(searchTerm, location, country_indeed);

      let raw;
      try {
        raw = execFileSync(PYTHON, ['-c', script], {
          timeout: 60000,
          maxBuffer: 10 * 1024 * 1024,
          encoding: 'utf8',
          stdio: ['pipe', 'pipe', 'pipe'],
        });
      } catch (err) {
        const stderr = err.stderr?.toString?.() ?? '';
        console.warn(`   ⚠️  Error en JobSpy para "${searchTerm}" @ "${location}": ${stderr.slice(0, 200)}`);
        continue;
      }

      let jobs;
      try {
        jobs = JSON.parse(raw.trim() || '[]');
      } catch {
        console.warn(`   ⚠️  JSON inválido de JobSpy para "${searchTerm}" @ "${location}"`);
        continue;
      }

      if (!Array.isArray(jobs)) {
        console.warn(`   ⚠️  Respuesta inesperada de JobSpy`);
        continue;
      }

      const filtered = jobs.filter(j => {
        if (!j.job_url) return false;
        if (seenUrls.has(j.job_url)) return false;
        if (!matchesFilter(j.title)) return false;
        return true;
      });

      console.log(`   ✅  ${filtered.length} nuevas (de ${jobs.length} totales) para "${searchTerm}" @ "${location}"`);

      for (const j of filtered) {
        seenUrls.add(j.job_url);
        newJobs.push({
          title: j.title ?? 'Unknown',
          company: j.company ?? 'Unknown',
          location: j.location ?? location,
          url: j.job_url,
          source: `jobspy-${sites.join('+')}`,
          market: label,
          date: j.date_posted ? String(j.date_posted).slice(0, 10) : new Date().toISOString().slice(0, 10),
        });
      }
    }
  }

  // --- Output ---
  console.log(`\n📊  Total nuevas ofertas encontradas: ${newJobs.length}`);

  if (newJobs.length === 0) {
    console.log('   No hay novedades. Pipeline sin cambios.');
    return;
  }

  // Print preview
  const previewN = Math.min(newJobs.length, 10);
  console.log(`\n   Primeras ${previewN} ofertas:`);
  for (const j of newJobs.slice(0, previewN)) {
    console.log(`   [${j.market}] ${j.title} @ ${j.company} — ${j.location}`);
    console.log(`         ${j.url}`);
  }
  if (newJobs.length > previewN) {
    console.log(`   ... y ${newJobs.length - previewN} más`);
  }

  if (dryRun) {
    console.log('\n   [dry-run] No se escribió nada.');
    return;
  }

  // Write to pipeline.md
  const today = new Date().toISOString().slice(0, 10);
  let pipelineLines = `\n## JobSpy scan — ${today} (${market.toUpperCase()}, ${sites.join('+')})\n\n`;
  for (const j of newJobs) {
    pipelineLines += `- [${j.market}] **${j.title}** @ ${j.company} (${j.location}) — ${j.url}\n`;
  }

  if (!existsSync(pipelinePath)) {
    writeFileSync(pipelinePath, `# Pipeline — Ofertas Pendientes\n`);
  }
  appendFileSync(pipelinePath, pipelineLines);

  // Write to scan-history.tsv
  const historyLines = newJobs
    .map(j => `${j.url}\t${j.title}\t${j.company}\t${j.source}\t${today}`)
    .join('\n') + '\n';

  if (!existsSync(historyPath)) {
    writeFileSync(historyPath, 'url\ttitle\tcompany\tsource\tdate\n');
  }
  appendFileSync(historyPath, historyLines);

  console.log(`\n✅  ${newJobs.length} ofertas agregadas a data/pipeline.md`);
  console.log(`   ${newJobs.length} URLs registradas en data/scan-history.tsv`);
  console.log('\n   Próximo paso: /career-ops pipeline para evaluar las ofertas nuevas\n');
}

runScan().catch(err => {
  console.error('❌  Error inesperado:', err.message);
  process.exit(1);
});
