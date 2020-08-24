# ------------------------------------------------- #
# Title: Assignment07.py
# Description: Working with Pickle module and Exceptions in Python3
# ChangeLog: (Who, When, What)
# Mercedes Gonzalez Gonzalez,8.23.2020>,Created Script
# ------------------------------------------------- #
import pickle
import random

# Data -------------------------------------------- #
customers_file_name = 'CustomerDataFile.txt'
customers_data = []

# Processing  --------------------------------------------------------------- #
class Processor():
    """  Performs Processing tasks """

    @staticmethod
    def deserialize_data_from_file(file_name, customers_list):
        """ Deserialize data from a file into a list of dictionary rows
        using Python Pickle module

        :param file_name: (string) with name of file:
        :param customers_list: (list) you want filled with file data:
        :return: (list) of dictionary rows
        """
        customers_list.clear()  # clear current data
        try:
            with open(file_name, "rb") as fh:
                try:
                    customers_list = pickle.load(fh)
                    message = "Data was successfully deserialized and loaded into customers list in memory!"
                    return customers_list, message
                except pickle.UnpicklingError:
                    error_message = """Error detected while trying to unpickle an object from file {}.
                    This could be due to the file might be corrupted, the file may contain non-serialized data
                    or an access violation. Initializing list of customers with empty list. """.format(file_name)
                    return [], error_message
        except FileNotFoundError:
            error_message = """Filename {} does not exist in the filesystem. 
            Initializing list of customers with empty list""".format(file_name)
            return [], error_message

    @staticmethod
    def serialize_data_to_file(file_name, customers_list):
        """ Serialize a list of dictionary rows to a file
        using Python Pickle module

        :param file_name: (string) with name of file:
        :param customers_list: (list) of dictionary rows containing customer data:
        :return: (tuple of boolean, string) indicating whether data was successfully serialized (True)
                 or not (False)
        """
        with open(file_name, "wb") as fh:
            try:
                pickle.dump(customers_list, fh)
                return True, 'Success'
            except pickle.PicklingError as e:
                error_message = """Error detected while trying to pickle object to file {}. Object is not pickable.
                Make sure the list of customers does not contain any non-pickable object such as: generators,
                inner classes, nested functions, lambda functions, defaultdicts, database connections, network sockets or 
                running threads. \nException occurred {}""".format(file_name, e)
                return False, error_message

    @staticmethod
    def add_customer(customer_id, customer_name, customers_list):
        if any(customer["ID"] == customer_id for customer in customers_list):
            return customers_list, """Error: Sorry, this customer cannot be added. Its customer ID is a duplicate value 
            of another customer already in the list. Please try re-adding it with a unique
            customer ID"""
        else:
            customers_list.append({"ID": customer_id, "Name": customer_name.strip()})
            return customers_list, 'Success'

    @staticmethod
    def remove_customer(customer_id, customers_list):
        found = False
        for row in customers_list:
            if customer_id == row["ID"]:
                customers_list.remove(row)
                found = True
                break
        if not found:
            return customers_list, 'Error: The customer ID you want to remove was not found'
        else:
            return customers_list, 'Success'

# Presentation (Input/Output)  -------------------------------------------- #
class IO:
    """ Performs Input and Output tasks """

    @staticmethod
    def print_menu():
        """  Display a menu of choices to the user

        :return: nothing
        """
        print("""
        Menu of Options
        1) Add a new Customer
        2) Remove an existing Customer
        3) Save Customers List to File        
        4) Reload Customers List from File
        5) Exit Program
        """)
        print()  # Add an extra line for looks

    @staticmethod
    def input_menu_choice():
        """ Gets the menu choice from a user

        :return: string
        """
        choice = str(input("Which option would you like to perform? [1 to 5] - ")).strip()
        print()  # Add an extra line for looks
        return choice

    @staticmethod
    def print_current_customers_in_list(customers_list):
        """ Shows the current customers in the list of dictionaries rows

        :param customers_list: (list) of rows you want to display
        :return: nothing
        """
        print("******* The current customers are: *******")
        for row in customers_list:
            print(str(row["ID"]) + " - (" + row["Name"] + ")")
        print("*******************************************")
        print()  # Add an extra line for looks

    @staticmethod
    def input_yes_no_choice(message):
        """ Gets a yes or no choice from the user

        :return: string
        """
        return str(input(message)).strip().lower()

    @staticmethod
    def input_press_to_continue(optional_message=''):
        """ Pause program and show a message before continuing

        :param optional_message:  An optional message you want to display
        :return: nothing
        """
        print(optional_message)
        input('Press the [Enter] key to continue.')

    @staticmethod
    def input_new_customer_id_and_name():
        try:
            customer_id = int(input("Please enter a new customer ID [1 to 10000]: "))
        except ValueError as e:
            customer_id = random.randint(1, 10000)
            print("""The customer ID you provided is not a valid integer number. \n
            A default random ID {} has been generated for the new customer. \n
            Exception occurred: {}""".format(customer_id, e))
        customer_name = input("Please enter a name for the new customer: ")
        return customer_id, customer_name

    @staticmethod
    def input_customer_id_to_remove():
        print("You have selected to remove an existing customer from the list")
        try:
            customer_id = int(input("Please, provide the ID of the customer you wish to remove [1 to 10000]: "))
        except ValueError() as e:
            customer_id = None
            print("""The customer ID you provided is not a valid integer number. \n
            Exception occurred: {}""".format(e))
        return customer_id


# Main Body of Script  ------------------------------------------------------ #

# Step 1 - When the program starts, Load data from CustomerDataFile.txt.
customers_data, result = Processor.deserialize_data_from_file(customers_file_name, customers_data)  # read file data
print(result)

# Step 2 - Display a menu of choices to the user
while (True):
    # Step 3 Show current data
    IO.print_current_customers_in_list(customers_data)  # Show current data in the customer list
    IO.print_menu()  # Shows menu
    strChoice = IO.input_menu_choice()  # Get menu option

    # Step 4 - Process user's menu choice
    if strChoice.strip() == '1':  # Add a new Customer
        new_c_id, new_c_name = IO.input_new_customer_id_and_name()
        customers_data, result = Processor.add_customer(new_c_id, new_c_name, customers_data)
        strStatus = "Your attempt to add a new customer to the list ended with the following result: {}".format(result)
        IO.input_press_to_continue(strStatus)
        continue  # to show the menu

    elif strChoice == '2':  # Remove an existing customer
        customer_id_to_remove = IO.input_customer_id_to_remove()
        if customer_id_to_remove:
            customers_data, result = Processor.remove_customer(customer_id_to_remove, customers_data)
            strStatus = "Your attempt to remove a task from the list ended with the following result: {}".format(result)
            IO.input_press_to_continue(strStatus)
        continue  # to show the menu

    elif strChoice == '3':  # Save Data to File
        strChoice = IO.input_yes_no_choice("Save this data to file? (y/n) - ")
        if strChoice.lower() == "y":
            result_b, result_message = Processor.serialize_data_to_file(customers_file_name, customers_data)
            strStatus = "Your attempt to save all data to a file ended with the following result: {}".format(result_message)
            IO.input_press_to_continue(strStatus)
        else:
            IO.input_press_to_continue("Save Cancelled!")
        continue  # to show the menu

    elif strChoice == '4':  # Reload Customer Data from File
        print("Warning: Unsaved Data Will Be Lost!")
        strChoice = IO.input_yes_no_choice("Are you sure you want to reload data from file? (y/n) -  ")
        if strChoice.lower() == 'y':
            customers_data, result = Processor.deserialize_data_from_file(customers_file_name, customers_data)
            strStatus = "Your attempt to reload data from file ended with the following result: {}".format(result)
            IO.input_press_to_continue(strStatus)
        else:
            IO.input_press_to_continue("File Reload  Cancelled!")
        continue  # to show the menu

    elif strChoice == '5':  # Exit Program
        print("Goodbye!")
        break  # and Exit
