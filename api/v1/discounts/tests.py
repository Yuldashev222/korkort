# from main.models import FileDetail
#
#
# def f(media_path):
#     import os
#     countries = os.listdir(media_path)  # ignore zip files and logos
#     cnt = 0
#     database_pdfs = FileDetail.objects.values_list('file', flat=True)
#     for country in countries:
#         if country == 'zip_files' or country == 'logos':
#             print(country)
#             continue
#         regions_path = os.path.join(media_path, country)
#         regions = os.listdir(regions_path)
#
#         for region in regions:
#             organs_path = os.path.join(regions_path, region)
#             organs = os.listdir(organs_path)
#
#             for organ in organs:
#                 file_dates_path = os.path.join(organs_path, organ)
#                 file_dates = os.listdir(file_dates_path)
#
#                 for file_date in file_dates:
#                     pdfs_path = os.path.join(file_dates_path, file_date)
#                     try:
#                         pdfs = os.listdir(pdfs_path)
#                     except NotADirectoryError:
#                         if file_date.endswith('.pdf'):
#                             pdf_path1 = os.path.join(pdfs_path, file_date)
#                             pdf_path = pdf_path1[pdfs_path.index('media') + 6:]
#                             if pdf_path not in database_pdfs:
#                                 print(pdf_path)
#                                 try:
#                                     os.remove(pdf_path1)
#                                 except Exception as e:
#                                     print(e)
#                                 cnt += 1
#                         continue
#
#                     for pdf in pdfs:
#                         pdf_path1 = os.path.join(pdfs_path, pdf)
#                         pdf_path = pdf_path1[pdfs_path.index('media') + 6:]
#                         if pdf_path not in database_pdfs:
#                             print(pdf_path)
#                             try:
#                                 os.remove(pdf_path1)
#                             except Exception as e:
#                                 print(e)
#                             cnt += 1

from django.db.models.functions
objects_with_slashes = CustomUser.objects.annotate(slash_count=Length(F('поле_со_слешами') - Length(F('поле_со_слешами'
                                                                                                      ).replace(Value('/'), Value(''))),
).filter(slash_count__gt=1000)