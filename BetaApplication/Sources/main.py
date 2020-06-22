"""
    Autor: Minnich Marian-Alin
    Data: 03.05.2020
"""


from facial_expression_recognition import FacialExpressionRecognition


if __name__ == "__main__":
    """ main
    Description:
        Metoda care instantiaza obiectul de tipul clasei FacialExpressionRecognition si care apeleaza metoda
        care contine thread-ul principal (main thread)

    Parameters:

    Returns:

    """

    my_obj = FacialExpressionRecognition()
    my_obj.run_task()


