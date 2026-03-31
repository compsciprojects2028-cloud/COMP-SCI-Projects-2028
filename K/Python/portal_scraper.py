import asyncio
import random
from pathlib import Path
from playwright.async_api import async_playwright

portal_url = "https://cuportal.covenantuniversity.edu.ng/login.php"

async def attendance_checker(url, username, password, modes: list, status_callback=None):
    sleep_timer = random.uniform(3, 5)
    
    def notify(msg):
        if status_callback:
            status_callback(msg)
            
    def set_html_and_css(element):
        css = """
            * {
                box-sizing: border-box;
            }

            body {
                margin: 0;
                padding: 16px;
                font-family: "Roboto", sans-serif, Helvetica, Arial, sans-serif;
                font-size: 13px;
                color: #313534;
                background: #fff;
                line-height: 1.846153846;
            }
            .form-group-row {
                position: relative;
                margin-bottom: 19px;
            }
            .col-sm-3 {
                width: 25%;
                float: left;
                position: relative;
                min-height: 1px;
                padding-left: 12px;
                padding-right: 12px;
            }
            .td-darkbg {
                background-color: darkgrey;
                color: white;
                width: 8em;
                height: 2em;
                font-size: small;
                text-align: center;
                vertical-align: middle;
                border: darkgrey solid 2px;
                white-space: nowrap;
            }
            .td-value {
                width: 5em;
                height: 2em;
                font-size: small;
                text-align: center;
                vertical-align: middle;
                border: darkgrey solid 2px;
                white-space: nowrap;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                margin-top: 10px;
            }
            thead th {
                text-align: left;
                font-weight: bold;
                padding: 10px 8px;
                border-bottom: 2px solid #dcdcdc;
                background-color: #ffffff;
            }
            tbody td {
                padding: 8px;
                vertical-align: top;
            }
            tbody tr:nth-child(even) {
                background-color: #f5f5f5;
            }
            tbody tr:nth-child(odd) {
                background-color: #ffffff;
            }
            
            @media print {
                body {
                    padding: 0;
                }

                table {
                    page-break-inside: auto;
                }

                tr {
                    page-break-inside: avoid;
                    break-inside: avoid;
                 }
            }


        """
        html = f"""
            <html>
                <head>
                <style>
                {css}
                </style>
                </head>
                <body>
                {element}
                </body>
            </html>
        """
        return html
    
    async with async_playwright() as p:
        notify("Launching Browser...")
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        
        notify("Opening portal...")
        await page.goto(url, wait_until="networkidle", timeout=0)
        
        notify("Logging in...")
        await page.locator("input[name='userid']").fill(username)
        await page.locator("input[name='inputpassword1']").fill(password)
        await page.click("input[type='submit']")
        await asyncio.sleep(sleep_timer)
        
        error_message = await page.locator("text=Username or Password Incorrect").is_visible()
        
        if error_message:
            await browser.close()
            raise ValueError("Invalid Username or Password")
        
        notify("Login successful")
        dashboard_url = page.url
        result_url = "https://resultprocessing.covenantuniversity.edu.ng/resultanalysis/studentresult.php"

        for mode in modes:
            if mode == "1" or mode == "2":
                await asyncio.sleep(sleep_timer)
                await page.click("text=attendance", timeout=0)
                await asyncio.sleep(sleep_timer)
        
            # Navigate to the attendance you want to check
            if mode == "1":
                notify("Fetching Lecture Attendance...")
                await page.click("text=Lecture Attendance Reports", timeout=0)
                await asyncio.sleep(sleep_timer)
                await page.click("text=Attendance Summay For Student", timeout=0) # lol typo
            
                # Get Lecture Attendance
                frame = page.frame_locator("iframe#frame")
                await frame.locator("div.col-md-10").wait_for(state="visible", timeout=0)
                await frame.locator("div.col-md-10").screenshot(path="lt_attendance.png")
                notify(f"lt_attendance.png saved to {Path.cwd()}")
                await page.goto(dashboard_url)
                
            
            elif mode == "2":
                notify("Fetching Chapel and Roll Call...")
                await page.click("text=Student Affairs Attendance", timeout=0)
                await asyncio.sleep(sleep_timer)
                await page.click("text=Attendance Summary For Student", timeout=0)
            
                frame = page.frame_locator("iframe#frame")
        
                # Get Chapel Attendance
                await frame.locator("div#upload-report").wait_for(state="visible", timeout=0)
                chapel_html = await frame.locator("div#upload-report").evaluate("el => el.outerHTML")
                new_page = await page.context.new_page()
                await new_page.set_content(set_html_and_css(chapel_html))
                await new_page.pdf(path="chapel_attendance.pdf", format="A4", print_background=True)
                await new_page.close()
                notify(f"chapel_attendance.png saved to {Path.cwd()}")
                    
                # Get Roll Call
                await frame.locator("li#event3").click()
                await asyncio.sleep(sleep_timer + 2)  # Waits for the Roll Call to load
                roll_call_html = await frame.locator("div#upload-report").evaluate("el => el.outerHTML")
                new_page = await page.context.new_page()
                await new_page.set_content(set_html_and_css(roll_call_html))
                await new_page.pdf(path="roll_call.pdf", format="A4", print_background=True)
                await new_page.close()
                notify(f"roll_call.png saved to {Path.cwd()}")
                await page.goto(dashboard_url)
            
            elif mode == "3":
                notify("Fetching results...")
                await asyncio.sleep(sleep_timer)
                await page.click("text=result processing", timeout=0)
                await asyncio.sleep(sleep_timer)
                
                # Get Result
                await page.goto(result_url, wait_until="networkidle", timeout=0)
                await page.pdf(path="result.pdf", format="A4", print_background=True)
                await page.goto(dashboard_url)
                
        notify("Done")
        await browser.close()
