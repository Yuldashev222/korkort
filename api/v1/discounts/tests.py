import os

media_path = 'path/to/media_file/'

countries = os.listdir(media_path)  # ignore zip files and logos
pdf_files_count = 0
database_pdfs = FileDetail.objects.values_list('')
for country in countries:
    regions_path = os.path.join(media_path, country)
    regions = os.listdir(regions_path)

    for region in regions:
        organs_path = os.path.join(regions_path, region)
        organs = os.listdir(organs_path)

        for organ in organs:
            file_dates_path = os.path.join(organs_path, organ)
            file_dates = os.listdir(file_dates_path)

            for file_date in file_dates:
                pdfs_path = os.path.join(file_dates_path, file_date)
                pdfs = os.listdir(pdfs_path)

                for pdf in pdfs:


