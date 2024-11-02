from sqlalchemy import Enum


class ResultEnum(str):
    win = "Cтавка выиграла"
    lose = "Ставка проиграла"

Result = Enum(ResultEnum.win, ResultEnum.lose, name="result_enum")