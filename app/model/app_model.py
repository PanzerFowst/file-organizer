import re


class Model:
    def __init__(self):
        pass

    # @property
    # def email(self) -> str:
    #     return self.__email

    # @email.setter
    # def email(self, value: str) -> None:
    #     """
    #     Validate the email
    #     :param value: The email address to validate and set
    #     :return: None
    #     """
    #     pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    #     if re.fullmatch(pattern, value):
    #         self.__email = value
    #     else:
    #         raise ValueError(f'Invalid email address: {value}')

    # def save(self) -> None:
    #     """
    #     Save the email into a file
    #     :return: None
    #     """
    #     with open('emails.txt', 'a') as f:
    #         f.write(self.email + '\n')
