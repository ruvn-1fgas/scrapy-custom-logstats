# Scrapy Custom LogStats

Custom Scrapy LogStats extension that automatically handles additional stats like pages/items per minute.

## Description

This repository provides a custom Scrapy LogStats extension that enhances the default logging by including additional statistics such as the number of pages and items processed per minute. This can be particularly useful for monitoring and optimizing web scraping performance.

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

