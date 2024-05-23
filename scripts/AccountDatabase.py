
#  Copyright (c) 华南理工大学学生创新团队 Last Update: 2024-05-23 21:33:27. All Rights Reserved.
#
#  @Project name and File name:Player_py - AccountDatabase.py
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are met:
#  Redistributions of source code must retain the above copyright notice,
#  this list of conditions and the following disclaimer.
#  Redistributions in binary form must reproduce the above copyright
#  notice, this list of conditions and the following disclaimer in the
#  documentation and/or other materials provided with the distribution.
#  Neither the name of the developer nor the names of its
#  contributors may be used to endorse or promote products derived from
#  this software without specific prior written permission.
#  重新分发和使用源代码和二进制形式的代码，无论是否进行修改，都是允许的，只要满足以下条件：
#  重新分发源代码时，必须保留上述版权通知、本条件列表以及以下免责声明。
#  以二进制形式重新分发时，必须在分发时提供的文档或其他材料中复制上述版权通知、本条件列表以及以下免责声明。
#  未经事先书面许可，不得使用开发者或贡献者的名称来认可或推广从本软件派生出来的产品。
#
#  Disclaimer
#  This software is provided "as is" without any express or implied warranty,
#  including but not limited to the warranties of merchantability,
#  fitness for a particular purpose, and non-infringement.
#  The risk of using this software lies with the user. The developers or contributors shall not be liable for any direct,
#  indirect, incidental, special, exemplary, or consequential damages resulting from the use of this software.
#  To the maximum extent permitted by law, the developers or contributors shall not be responsible for any claims,
#  losses, liabilities, damages, costs, or expenses arising from the use or inability to use this software.
#  免责声明
#  本软件按“现状”提供，不附带任何形式的明示或暗示保证，包括但不限于对适销性、特定用途的适用性或非侵权性的保证。
#  使用本软件的风险由用户自行承担。开发者或贡献者不对因使用本软件而导致的任何直接、间接、偶然、特殊、惩戒性或后果性损害承担任何责任。
#  在法律允许的最大范围内，开发者或贡献者对于因使用或无法使用本软件而产生的任何索赔、损失、责任、损害、成本或费用均不承担责任。

# coding = UTF-8

from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlError
from PyQt5.QtCore import QThread

class Intent():
    def __init__(self):
        self.configFileName = ""
        self.passwordCorrect = False
        self.IDCorrect = False
        self.selectFinished = False
        self.InsertSuccess = False
    
    def Reset(self):
        self.configFileName = ""
        self.passwordCorrect = False
        self.IDCorrect = False
        self.selectFinished = False
        self.InsertSuccess = False

IntentHelper = Intent()

class InsertDatabase(QThread):  #进行数据插入操作
    def __init__(self, account, password, filePath):
        super().__init__()
        self.account = account
        self.password = password
        self.filePath = filePath

    def run(self):
        try:
            # 连接到 SQLite 数据库（如果数据库不存在，将创建它）
            db = QSqlDatabase.addDatabase("QSQLITE")
            db.setDatabaseName("accounts.db")
            if not db.open():
                error = db.lastError()
                print(error.text())
                return
            query = QSqlQuery()
            if not query.exec_("CREATE TABLE IF NOT EXISTS accounts (id TEXT PRIMARY KEY,"
                            "password TEXT NOT NULL,"
                            "filepath TEXT NOT NULL)"):  #如果表不存在则建表
                error = query.lastError()
                print(f"Error creating table: {error.text()}")
                return
            # 插入数据的 SQL 语句
            sql_insert = """
            INSERT INTO accounts (id, password, filepath)
            VALUES (:id, :password, :filepath)
            """
            query.prepare(sql_insert)
            query.bindValue(":id", self.account)
            query.bindValue(":password", self.password)
            query.bindValue(":filepath", self.filePath)
            # 执行 SQL 语句
            if not query.exec_():
                error = query.lastError()
                if error.type() == QSqlError.ConnectionError:
                    # 主键冲突，打印错误信息
                    print(f"Constraint violation occurred: {error.text()}")
                    IntentHelper.IDCorrect = False
                else:
                    IntentHelper.IDCorrect = True #出现其他错误
                    print(f"Error inserting data: {error.text()}")
            else:
                IntentHelper.InsertSuccess = True
                IntentHelper.IDCorrect = True
            IntentHelper.selectFinished = True
            db.close()
        except Exception as e:
            # 这里捕获的是运行时错误，而不是数据库错误
            print(f"An unexpected error occurred: {e}")


class SelectDatabase(QThread):  #查询操作
    def __init__(self, account, password):
        super().__init__()
        self.account = account
        self.password = password
        global IntentHelper
    
    def run(self):
        try:
            # 连接到 SQLite 数据库
            db = QSqlDatabase.addDatabase("QSQLITE")
            db.setDatabaseName("accounts.db")
            if not db.open():
                error = db.lastError()
                print(error.text())
                return
            query = QSqlQuery()
            sql_select = """
            SELECT password, filepath FROM accounts WHERE id = :id
            """
            query.prepare(sql_select)
            query.bindValue(":id", self.account)
            if query.exec_():
                # 检查是否有结果返回
                if query.next():
                    # 获取数据库中的密码和文件路径
                    db_password = query.value(0)  # 密码字段的值
                    filepath = query.value(1)  # 文件路径字段的值
                    IntentHelper.IDCorrect = True
                    # 比较密码
                    if self.password == db_password:
                        IntentHelper.passwordCorrect = True
                        IntentHelper.configFileName = filepath
                    else:
                        print("Password does not match.")
                else:
                    print("No record found for the given ID.")
            else:
                error = query.lastError()
                print(f"Error executing query: {error.text()}")
            IntentHelper.selectFinished = True
            db.close()
        except Exception as e:
            # 这里捕获的是运行时错误，而不是数据库错误
            print(f"An unexpected error occurred: {e}")
    

class UpadateDatabase(QThread):
    def __init__(self, account, newPassword):
        super().__init__()
        self.account = account
        self.newPassword = newPassword
        
    def run(self):
        try:
            # 连接到 SQLite 数据库
            db = QSqlDatabase.addDatabase("QSQLITE")
            db.setDatabaseName("accounts.db")
            if not db.open():
                error = db.lastError()
                print(error.text())
                return
            query = QSqlQuery()
            sql_select = """
            UPDATE accounts
            SET password = :newpassword
            WHERE id = :idToUpdate
            """
            query.prepare(sql_select)
            query.bindValue(":newpassword", self.newPassword)
            query.bindValue(":idToUpdate", self.account)
            if query.exec_():
                # 检查是否有结果返回
                if query.numRowsAffected() > 0:
                    IntentHelper.IDCorrect = True
                else:
                    pass
            else:
                error = query.lastError()
                print(error.text())
            IntentHelper.selectFinished = True
            db.close()
        except Exception as e:
            print(f"An unexpected error occurred: {e}")