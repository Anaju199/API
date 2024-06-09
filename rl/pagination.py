from rest_framework.pagination import PageNumberPagination

class CustomPagination(PageNumberPagination):
    page_size_query_param = '_limit'  # Define o parâmetro que será usado para o tamanho da página
    page_query_param = '_page'  # Define o parâmetro que será usado para a página
