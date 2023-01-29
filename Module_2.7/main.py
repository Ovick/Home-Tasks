from seed import prepare_data, generate_fake_data, insert_data_to_db, \
    NUMBER_FACULTIES, NUMBER_STUDENTS, NUMBER_DISCIPLINES, NUMBER_TEACHERS
import my_select


def print_query_result(query_output: list) -> None:
    column_names = dict().fromkeys(query_output[0])
    print("\t".join(column_names))
    row_as_str = ""
    for row in query_output:
        for value in row.values():
            row_as_str += str(value)+"\t"
        row_as_str += "\n"
    print(row_as_str)


if __name__ == "__main__":
    # university db should be created previously with alembic from db_model.py
    # seed random values
    faculties, students, teachers, disciplines, marks = prepare_data(
        *generate_fake_data(NUMBER_FACULTIES, NUMBER_STUDENTS, NUMBER_DISCIPLINES, NUMBER_TEACHERS))
    insert_data_to_db(faculties, students, teachers, disciplines, marks)
    # execute the query
    print_query_result(my_select.select_1())
    print_query_result(my_select.select_2())
    print_query_result(my_select.select_3())
    print_query_result(my_select.select_4())
    print_query_result(my_select.select_5())
    print_query_result(my_select.select_6())
    print_query_result(my_select.select_7())
    print_query_result(my_select.select_8())
    print_query_result(my_select.select_9())
    print_query_result(my_select.select_10())
    print_query_result(my_select.select_11())
