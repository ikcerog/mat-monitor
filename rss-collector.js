const Parser = require('rss-parser');
const { convert } = require('html-to-text');
const fs = require('fs').promises;
const path = require('path');

const parser = new Parser({
  customFields: {
    item: ['content:encoded', 'description', 'summary']
  }
});

// Configuration
const CONFIG_FILE = path.join(__dirname, 'rss-config.json');
const OUTPUT_FILE = path.join(__dirname, 'summary_cache.txt');

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
 * Fetch and parse a single RSS feed
 */
async function fetchFeed(feedConfig) {
  try {
    console.log(`Fetching: ${feedConfig.name} (${feedConfig.url})`);
    const feed = await parser.parseURL(feedConfig.url);
    return { success: true, feed, config: feedConfig };
  } catch (error) {
    console.error(`Error fetching ${feedConfig.name}:`, error.message);
    return { success: false, error: error.message, config: feedConfig };
  }
}

/**
 * Process feed items into clean text
 */
function processFeedItems(feed, config, settings) {
  const items = feed.items.slice(0, settings.maxArticlesPerFeed || 10);
  let output = `\n${'='.repeat(80)}\n`;
  output += `FEED: ${feed.title || config.name}\n`;
  output += `SOURCE: ${config.url}\n`;
  output += `${'='.repeat(80)}\n\n`;

  items.forEach((item, index) => {
    output += `Article ${index + 1}: ${item.title || 'Untitled'}\n`;
    output += `Published: ${item.pubDate || 'Unknown date'}\n`;

    if (item.link) {
      output += `Link: ${item.link}\n`;
    }

    output += `\n`;

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
      output += `${content}\n`;
    }

    output += `\n${'-'.repeat(80)}\n\n`;
  });

  return output;
}

/**
 * Format current date/time
 */
function getFormattedDateTime() {
  const now = new Date();
  const month = String(now.getMonth() + 1).padStart(2, '0');
  const day = String(now.getDate()).padStart(2, '0');
  const year = now.getFullYear();

  let hours = now.getHours();
  const minutes = String(now.getMinutes()).padStart(2, '0');
  const seconds = String(now.getSeconds()).padStart(2, '0');
  const ampm = hours >= 12 ? 'PM' : 'AM';

  hours = hours % 12;
  hours = hours ? hours : 12; // the hour '0' should be '12'
  const hoursStr = String(hours).padStart(2, '0');

  return `${month}/${day}/${year} at ${hoursStr}:${minutes}:${seconds} ${ampm}`;
}

/**
 * Main function
 */
async function main() {
  console.log('RSS Feed Collector Starting...\n');

  // Load configuration
  const config = await loadConfig();
  const enabledFeeds = config.feeds.filter(f => f.enabled !== false);

  console.log(`Found ${enabledFeeds.length} enabled feeds\n`);

  // Fetch all feeds
  const feedResults = await Promise.all(
    enabledFeeds.map(feedConfig => fetchFeed(feedConfig))
  );

  // Process successful feeds
  const successfulFeeds = feedResults.filter(r => r.success);
  console.log(`\nSuccessfully fetched ${successfulFeeds.length}/${enabledFeeds.length} feeds\n`);

  // Build output content
  let output = `Last updated: ${getFormattedDateTime()}\n`;
  output += `${'='.repeat(80)}\n`;
  output += `RSS FEED COMPILATION\n`;
  output += `Total feeds processed: ${successfulFeeds.length}\n`;
  output += `${'='.repeat(80)}\n`;

  successfulFeeds.forEach(result => {
    output += processFeedItems(result.feed, result.config, config.settings);
  });

  // Add summary at the end
  output += `\n${'='.repeat(80)}\n`;
  output += `END OF COMPILATION\n`;
  output += `Last updated: ${getFormattedDateTime()}\n`;
  output += `${'='.repeat(80)}\n`;

  // Write to file
  await fs.writeFile(OUTPUT_FILE, output, 'utf8');
  console.log(`✓ Output written to ${OUTPUT_FILE}`);
  console.log(`✓ Total size: ${(output.length / 1024).toFixed(2)} KB`);

  // Report any failures
  const failedFeeds = feedResults.filter(r => !r.success);
  if (failedFeeds.length > 0) {
    console.log('\nFailed feeds:');
    failedFeeds.forEach(f => {
      console.log(`  - ${f.config.name}: ${f.error}`);
    });
  }

  console.log('\n✓ RSS Collection Complete!');
}

// Run main function
main().catch(error => {
  console.error('Fatal error:', error);
  process.exit(1);
});
