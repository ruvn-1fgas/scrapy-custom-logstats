# Scrapy Custom LogStats

Custom Scrapy LogStats extension that automatically handles additional stats like pages/items per minute.

## Features

- Automatic logging of additional statistics like:
  - `products`
  - `reviews`
  - `categories`
- Easy integration with existing Scrapy projects

## Usage

To use the custom LogStats extension in your Scrapy project, add the following settings to your `settings.py`:

```py
EXTENSIONS = {
    'scrapy_custom_logstats.LogStats': 500,
}
```

## Increasing Stats

You can increase custom statistics in your spider by using the following code:

```py
self.crawler.stats.inc_value(f"{stat_name}_scraped_count", spider=self)
```

Replace `stat_name` with the name of the stat you want to increase.

