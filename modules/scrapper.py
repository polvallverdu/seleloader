from playwright.async_api import async_playwright, Playwright, Browser, Page

class Scrapper:
  
  def __init__(self, playwright: Playwright, browser: Browser):
    self.playwright = playwright
    self.browser = browser
    self.page = None
  
  async def goto(self, url: str) -> None:
    if not self.page:
      self.page = await self.browser.new_page()
    await self.page.goto(url)
  
  async def content(self, url: str) -> str:
    temppage = await self.browser.new_page()
    await temppage.goto(url)
    content = await temppage.content()
    await temppage.close(run_before_unload=True)
    return content
  
  async def extract_exam_data(self) -> list[dict]:
    exam_data = []
    cards = await self.page.query_selector_all('.card.mb-4.results-item')
    
    for card in cards:
        url_element = await card.query_selector("a[itemprop='url mainEntityOfPage']")
        url = await url_element.get_attribute("href")
        exam_id = url.split('/')[-2]
        subject = await (await card.query_selector("span[itemprop='articleSection']")).inner_text()
        location = await (await card.query_selector("span[itemprop='author']")).inner_text()
        date = await (await card.query_selector("span[itemprop='headline']")).inner_text()
        exam_data.append({
            "id": exam_id,
            "subject": subject,
            "location": location,
            "date": date
        })
    return exam_data

  async def shutdown(self):
    await self.browser.close()
    self.playwright.stop()

async def create_scrapper(headless: bool=True) -> Scrapper:
  pw = await async_playwright().start()
  browser = await pw.chromium.launch(
    headless=headless,
    ignore_default_args=["--mute-audio"]
  )
  return Scrapper(pw, browser)

