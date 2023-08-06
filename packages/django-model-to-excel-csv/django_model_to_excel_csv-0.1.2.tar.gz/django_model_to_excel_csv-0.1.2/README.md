Simple Excel and CSV File Generator From Django Model.

Required Packages:

    pip install pandas

Usage :

Django Models to Excel File:

    from django_model_to_excel_csv import generate_excel_file

    def func(request):
        queryset = User.objects.all().values()
        # queryset will be your model data
        # file_path : 'your absloute path' or it will store in your project Base Directory
        # file_name accepts string : 'string' 
        # sheet_name accepts string : 'string'
        # index and header : Boolean
        generate_excel = generate_excel_file.all_to_excel(queryset, file_path, file_name, sheet_name, index, header)


Django Models to CSV File:

    from django_model_to_excel_csv import generate_csv_file

    def func(request):
        queryset = User.objects.all().values()
        # queryset will be your model data
        # file_path : 'your absloute path' or it will store in your project Base Directory
        # file_name accepts string : 'string' 
        # sheet_name accepts string : 'string'
        # index and header : Boolean
        generate_excel = generate_excel_file.all_to_excel(queryset, file_path, file_name, sheet_name, index, header)
        


