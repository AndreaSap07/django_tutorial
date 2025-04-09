from django.shortcuts import render, redirect
#import io
import requests
from django.http import HttpResponse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import pandas as pd
from .models import PassItem
import csv
from django.utils.dateparse import parse_datetime




# Create your views here.

# This renders the download page
def download_page_view(request):
    return render(request, 'download_page.html')


def dl_geov_view(request):

    # Setup Selenium headless browser
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    index_url = 'http://10.5.129.79/mfz/events.html'  # Marco's website

        # If you use webdriver-manager (recommended)
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        index_url = 'http://10.5.129.79/mfz/events.html'  # Marco's website
        driver.get(index_url)

        # Wait for JavaScript to load — simple pause or use WebDriverWait
        time.sleep(3)  # For demo; replace with proper waits if needed

        # Find all .xml links
        xml_links = []
        links = driver.find_elements(By.TAG_NAME, 'a')
        for link in links:
            href = link.get_attribute('href')
            if href and href.endswith('.xml'):
                xml_links.append(href)

        xml_links = xml_links[:2]  # Only take first 2

    finally:
        driver.quit()  # Always clean up the driver

    if not xml_links:
        return HttpResponse("No XML files found.", status=404)

    for xml_url in xml_links:
        response = requests.get(xml_url)
        if response.status_code == 200:
            try:
                # Read XML file
                namespaces = {"cf": "http://eop-cfi.esa.int/CFI"}
                df = pd.read_xml(xml_url, xpath=".//cf:Event", namespaces=namespaces)
                
                event_types_to_keep = ["STAT_VIS_Z"]  #STAT_VIS_Z should be AOS0!!!
                # Filter AOS
                filtered_df = df[df["Event_Type"].isin(event_types_to_keep)]
                filtered_df["UTC_Start_Time"] = pd.to_datetime(filtered_df["UTC_Start_Time"])

                #print(filtered_df)
                rows = []
                for _, row in filtered_df.iterrows():
                    rows.append(PassItem(
                        utc_start_time=row.get("UTC_Start_Time", ''),
                        antenna=row.get("Entity", ''),
                        orbit_num=row.get('Abs_Orb_No', 0),
                        satellite=row.get('Sat', ''),
                        source_file=xml_url.split('/')[-1]
                    ))
                PassItem.objects.bulk_create(rows)
            except Exception as e:
                print(f"Failed to parse {xml_url}: {e}")

    return redirect('filter_page')


def filter_page_view(request):
    entity_choices = ["SDA4", "SDA5", "MCM", "DBA1", "TTC3"]
    
    selected_antennas = request.GET.getlist("antenna")
    start = request.GET.get("start_date")
    end = request.GET.get("end_date")

    queryset = PassItem.objects.all()

    if selected_antennas:
        queryset = queryset.filter(antenna__in=selected_antennas)
    
    if start:
        queryset = queryset.filter(utc_start_time__gte=parse_datetime(start))
    if end:
        queryset = queryset.filter(utc_start_time__lte=parse_datetime(end))

    context = {
        "PassItems": queryset,
        "entity_choices": entity_choices,
        "selected_antennas": selected_antennas,
        "start_date": start,
        "end_date": end,
    }
    return render(request, "filter_page.html", context)



def export_csv_view(request):
    selected_categories = request.GET.getlist('antenna')
    items = PassItem.objects.filter(category__in=selected_categories) if selected_categories else PassItem.objects.all()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="filtered_items.csv"'
    writer = csv.writer(response)
    writer.writerow(['Start Time', 'antenna', 'Orbit Num', 'Satellite'])

    for item in items:
        writer.writerow([item.utc_start_time, item.antenna, item.orbit_num, item.satellite])

    return response
"""
    # Download and zip the XML files
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        for i, xml_url in enumerate(xml_links):
            response = requests.get(xml_url)
            filename = xml_url.split('/')[-1] or f'file{i+1}.xml'
            if response.status_code == 200:
                zip_file.writestr(filename, response.content)
            else:
                zip_file.writestr(filename, f"Failed to download {xml_url}")

    zip_buffer.seek(0)
    return HttpResponse(
        zip_buffer.read(),
        content_type='application/zip',
        headers={'Content-Disposition': 'attachment; filename="xml_files.zip"'}
    )
    """
