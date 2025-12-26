const Parser = require('rss-parser');
const { convert } = require('html-to-text');
const fs = require('fs').promises;
const path = require('path');

const parser = new Parser({
  customFields: {
    item: ['content:encoded', 'description', 'summary']
  },
  timeout: 30000 // 30 second timeout per feed
});

// Configuration
const CONFIG_FILE = path.join(__dirname, 'rss-config.json');
const OUTPUT_FILE = path.join(__dirname, 'summary_cache.txt');
const FEED_TIMEOUT = 30000; // 30 seconds

/**
 * Load RSS feeds configuration
 */
async function loadConfig() {
  try {
    const data = await fs.readFile(CONFIG_FILE, 'utf8');
    return JSON.parse(data);
  } catch (error) {
    console.error('Error loading config:', error.message);
    process.exit(1);
  }
}

/**
 * Convert HTML to clean text
 */
function htmlToCleanText(html) {
  if (!html) return '';

  return convert(html, {
    wordwrap: false,
    selectors: [
      { selector: 'a', options: { ignoreHref: true } },
      { selector: 'img', format: 'skip' },
      { selector: 'script', format: 'skip' },
      { selector: 'style', format: 'skip' }
    ]
  }).trim();
}

/**
 * Fetch and parse a single RSS feed with timeout
 */
async function fetchFeed(feedConfig, index, total) {
  const startTime = Date.now();
  try {
    console.log(`[${index}/${total}] Fetching: ${feedConfig.name}...`);

    // Race between feed fetch and timeout
    const feed = await Promise.race([
      parser.parseURL(feedConfig.url),
      new Promise((_, reject) =>
        setTimeout(() => reject(new Error('Timeout')), FEED_TIMEOUT)
      )
    ]);

    const duration = ((Date.now() - startTime) / 1000).toFixed(1);
    const articleCount = feed.items?.length || 0;
    console.log(`[${index}/${total}] ✓ ${feedConfig.name} - ${articleCount} articles (${duration}s)`);

    return { success: true, feed, config: feedConfig };
  } catch (error) {
    const duration = ((Date.now() - startTime) / 1000).toFixed(1);
    console.error(`[${index}/${total}] ✗ ${feedConfig.name} - ${error.message} (${duration}s)`);
    return { success: false, error: error.message, config: feedConfig };
  }
}

/**
 * Process feed items into clean text
 */
function processFeedItems(feed, config, settings) {
  const items = feed.items.slice(0, settings.maxArticlesPerFeed || 10);
  let output = `\nFEED: ${feed.title || config.name}\n`;
  output += `SOURCE: ${config.url}\n\n`;

  items.forEach((item, index) => {
    output += `${item.title || 'Untitled'}\n`;
    output += `Published: ${item.pubDate || 'Unknown date'}\n`;

    if (item.link) {
      output += `${item.link}\n`;
    }

    // Get content - try multiple fields
    let content = '';
    if (settings.includeContent && item['content:encoded']) {
      content = htmlToCleanText(item['content:encoded']);
    } else if (settings.includeContent && item.content) {
      content = htmlToCleanText(item.content);
    } else if (settings.includeDescription && item.description) {
      content = htmlToCleanText(item.description);
    } else if (item.summary) {
      content = htmlToCleanText(item.summary);
    } else if (item.contentSnippet) {
      content = item.contentSnippet;
    }

    if (content) {
      output += `\n${content}\n`;
    }

    output += `\n`;
  });

  return output;
}

/**
 * Format current date/time in Eastern Time (Detroit)
 */
function getFormattedDateTime() {
  const now = new Date();

  // Convert to Eastern Time (America/Detroit)
  const options = {
    timeZone: 'America/Detroit',
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    hour12: true
  };

  const formatter = new Intl.DateTimeFormat('en-US', options);
  const parts = formatter.formatToParts(now);

  // Extract parts
  const partsMap = {};
  parts.forEach(part => {
    partsMap[part.type] = part.value;
  });

  return `${partsMap.month}/${partsMap.day}/${partsMap.year} at ${partsMap.hour}:${partsMap.minute}:${partsMap.second} ${partsMap.dayPeriod}`;
}

/**
 * Main function
 */
async function main() {
  const startTime = Date.now();
  console.log('━'.repeat(80));
  console.log('RSS Feed Collector Starting...');
  console.log('━'.repeat(80));
  console.log('');

  // Load configuration
  const config = await loadConfig();
  const enabledFeeds = config.feeds.filter(f => f.enabled !== false);

  console.log(`📋 Configuration loaded: ${enabledFeeds.length} enabled feeds`);
  console.log(`⏱️  Timeout per feed: ${FEED_TIMEOUT / 1000}s`);
  console.log('');
  console.log('━'.repeat(80));
  console.log('FETCHING FEEDS');
  console.log('━'.repeat(80));
  console.log('');

  // Fetch all feeds with progress tracking
  const feedResults = await Promise.all(
    enabledFeeds.map((feedConfig, index) =>
      fetchFeed(feedConfig, index + 1, enabledFeeds.length)
    )
  );

  const fetchDuration = ((Date.now() - startTime) / 1000).toFixed(1);

  // Process successful feeds
  const successfulFeeds = feedResults.filter(r => r.success);
  console.log('');
  console.log('━'.repeat(80));
  console.log(`FETCH COMPLETE - ${successfulFeeds.length}/${enabledFeeds.length} succeeded (${fetchDuration}s)`);
  console.log('━'.repeat(80));
  console.log('');

  // Build output content
  console.log('📝 Processing feed content...');
  let output = `Last updated: ${getFormattedDateTime()}\n`;
  output += `Total feeds: ${successfulFeeds.length}\n`;

  let totalArticles = 0;
  successfulFeeds.forEach((result, index) => {
    const articleCount = result.feed.items?.slice(0, config.settings.maxArticlesPerFeed || 10).length || 0;
    totalArticles += articleCount;
    console.log(`   Processing [${index + 1}/${successfulFeeds.length}]: ${result.config.name} (${articleCount} articles)`);
    output += processFeedItems(result.feed, result.config, config.settings);
  });

  console.log('');
  console.log('━'.repeat(80));
  console.log('WRITING OUTPUT');
  console.log('━'.repeat(80));

  // Write to file
  await fs.writeFile(OUTPUT_FILE, output, 'utf8');
  const fileSizeKB = (output.length / 1024).toFixed(2);
  const totalDuration = ((Date.now() - startTime) / 1000).toFixed(1);

  console.log(`✓ File written: ${OUTPUT_FILE}`);
  console.log(`✓ File size: ${fileSizeKB} KB`);
  console.log(`✓ Total articles: ${totalArticles}`);
  console.log(`✓ Total duration: ${totalDuration}s`);

  // Report any failures
  const failedFeeds = feedResults.filter(r => !r.success);
  if (failedFeeds.length > 0) {
    console.log('');
    console.log('━'.repeat(80));
    console.log(`FAILED FEEDS (${failedFeeds.length})`);
    console.log('━'.repeat(80));
    failedFeeds.forEach(f => {
      console.log(`  ✗ ${f.config.name}: ${f.error}`);
    });
  }

  console.log('');
  console.log('━'.repeat(80));
  console.log('✓ RSS COLLECTION COMPLETE!');
  console.log('━'.repeat(80));
}

// Run main function
main().catch(error => {
  console.error('Fatal error:', error);
  process.exit(1);
});
