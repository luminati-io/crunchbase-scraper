# Setting Up the Bright Data Crunchbase Scraper

This guide provides step-by-step instructions on how to set up and use the Bright Data Web Scraper for Crunchbase. You can leverage Bright Data's powerful infrastructure to collect data from Crunchbase profiles either programmatically via API or through a user-friendly no-code interface.

**Prerequisites:**

* An active Bright Data account.

## Steps

1.  **Log in to Bright Data:**
    Access your Bright Data dashboard.
2.  **Navigate to Web Scrapers Library:**
    * Select the **Web Scrapers** tab in the left-hand menu.
    * Choose the **Web Scrapers Library** sub-tab.

    ![Bright Data Dashboard](https://github.com/user-attachments/assets/f680db57-a15a-4bd9-8dfc-f7cab5e3219b)

3.  **Find the Crunchbase Scraper:**
    * Use the search bar and type "crunchbase".
    * Select the **crunchbase.com** scraper from the search results.

    ![Search for Crunchbase Scraper](https://github.com/user-attachments/assets/faf6ef56-859c-4cd9-baef-ace81d6cfe1d)

4.  **Choose Scraper Type:**
    You'll see different scraper templates available for Crunchbase. This guide focuses on the **Collect by URL** option. Select it.

    ![Select Collect by URL](https://github.com/user-attachments/assets/fc1cc4dc-b637-44db-b782-81a9be0cf92f)

5.  **Select Interaction Method:**
    Bright Data offers two ways to use the scraper:
    * **Scraper APIs:** For programmatic integration into your applications.
    * **No-code scraper:** For a user-interface-driven approach without writing code.

    Choose the method that best suits your needs and select **Next**.

    ![Choose Scraper API or No-code](https://github.com/user-attachments/assets/3b9518a2-ce00-4e90-9f8b-44ff3be30d54)

### Option A: Using the Scraper API

If you selected **Scraper APIs**, you'll be directed to the API configuration dashboard.

![Crunchbase Scraper API Dashboard](https://github.com/user-attachments/assets/63e80d6e-5c57-4f2e-8d3c-300baa5f43a1)

**Configuration and Usage:**

1.  **API Request Builder:**
    * **Inputs:** Add the specific Crunchbase URLs you want to scrape.
    * **Output Format:** Select the desired data format (JSON, CSV).
    * **Data Delivery:** Configure how you want to receive the data:
        * [Deliver to External Storage](https://docs.brightdata.com/scraping-automation/web-scraper-api/overview#via-deliver-to-external-storage%3A) (e.g., Email, S3, Google Cloud Storage, SFTP).
        * [Send to Webhook](https://docs.brightdata.com/scraping-automation/web-scraper-api/overview#via-webhook%3A).
    * **Notifications:** Set up URLs to be notified upon job completion or failure.

2.  **Running the Scraper:**
    * As you adjust the settings, the request builder on the right side updates automatically.
    * It provides a ready-to-use **cURL command** or code snippets in various programming languages (Python, Node.js, Java, C#, PHP, etc.).
    * Copy the generated code and execute it from your terminal or integrate it into your application.

3.  **Additional Features:**
    * **Overview Tab:** General information about your API usage.
    * **Management APIs Tab:** APIs to manage your scraper instances programmatically.
    * **Logs Tab:** Detailed logs of your API requests and scraper runs.

For a comprehensive overview of all settings, refer to the [Web Scraper API Documentation](https://docs.brightdata.com/scraping-automation/web-scraper-api/overview).

### Option B: Using the No-code Scraper

If you selected **No-code scraper**, you'll be presented with a user-friendly interface for configuration.

**Configuration and Execution:**

1.  **Input URLs:**
    * Paste multiple Crunchbase URLs directly into the input field (one URL per line).
    * Alternatively, **upload a CSV file** containing a list of URLs.

2.  **Data Delivery Settings:**
    * Configure how and where your data should be delivered (e.g., Email, cloud storage).
    * Select the delivery settings toggle to configure. See [Data Delivery Settings](https://docs.brightdata.com/scraping-automation/web-scraper-api/overview#via-deliver-to-external-storage%3A) for details.

3.  **Start and Download:**
    * Once your inputs and delivery settings are configured, select the **Start collecting** button.

      ![No-code Scraper Input Configuration](https://github.com/user-attachments/assets/ee2b3bc4-9d42-45c2-99f2-e9387548ff26)

    * When collection is complete, download the data in your preferred format (JSON, CSV, JSONL, or NDJSON).
    
      ![Download Data Options](https://github.com/user-attachments/assets/f3fd94f3-c995-46a5-aaaa-3f5ad3361e4c)
