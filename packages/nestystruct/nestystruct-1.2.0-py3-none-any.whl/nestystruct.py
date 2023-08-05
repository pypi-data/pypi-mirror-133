"""Este é o módulo "nestystruct.py" e fornece uma função chamada print_list() 
que imprime listas que podem ou não conter listas aninhadas.

This is the "nestystruct.py" module and it provides one function called print_list() 
which prints lists that may or may not include nested lists."""

def print_list(the_list,level=0):
    """Esta função requer um argumento posicional chamado "the_list", que é
    qualquer lista Python (de possíveis listas aninhadas). Cada item de dados na
    lista fornecida é (recursivamente) impresso na tela em sua própria linha.
    Um segundo argumento chamado "level" é usado para inserir tabulações quando
    uma lista aninhada é encontrada.
    
    This function takes one positional argument called "the_list", which is
    any Python list (of possibly nested lists). Each data item in the
    provided list is (recursively) printed to the screen on its own line.
    A second argument called "level" is used to insert tabulations when a 
    nested list is found."""
    
    for each_item in the_list:
        if isinstance(each_item,list):
            print_list(each_item,level+1)
        else:
            for tab_ in range(level):
                print("\t",end=' ')
            print(each_item)
