import json
import typing

import mysql.connector


class Recorder:
    def __del__(self) -> None:
        self.databaseConnection.close()


    def __init__(self) -> None:
        with open('config.json') as f:
            self.configuration = json.load(f)
        self.establishDatabaseConnection()
        self.initializeDatabase()


    def establishDatabaseConnection(self) -> bool:
        try:
            self.databaseConnection = mysql.connector.connect(
                database = self.configuration['databaseName'],
                host = self.configuration['databaseHost'],
                user = self.configuration['databaseUsername'],
                password = self.configuration['databasePassword'],
                port = self.configuration['databasePort'],
                buffered = True
            )
        except:
            return False


    def initializeDatabase(self) -> bool:
        status = True

        status = status and self.executeDatabaseQuery(
            '''
            CREATE TABLE IF NOT EXISTS user (
            userID VARCHAR(20),
            permission INT UNSIGNED,
            daily INT UNSIGNED,
            scrap INT UNSIGNED,
            hanging BOOLEAN,
            PRIMARY KEY (userID));
            '''
        )[0]

        status = status and self.executeDatabaseQuery(
            '''
            CREATE TABLE IF NOT EXISTS boss (
            bossID INT UNSIGNED,
            bossStage INT UNSIGNED,
            bossHP INT UNSIGNED,
            PRIMARY KEY (bossID, bossStage));
            '''
        )[0]

        status = status and self.executeDatabaseQuery(
            '''
            CREATE TABLE IF NOT EXISTS current (
            bossID INT UNSIGNED,
            bossStage INT UNSIGNED,
            bossHP INT UNSIGNED,
            PRIMARY KEY (bossID));
            '''
        )[0]

        status = status and self.executeDatabaseQuery(
            '''
            CREATE TABLE IF NOT EXISTS battle (
            bossID INT UNSIGNED,
            playerID VARCHAR(20),
            PRIMARY KEY (bossID, playerID));
            '''
        )[0]

        status = status and self.executeDatabaseQuery(
            '''
            CREATE TABLE IF NOT EXISTS record (
            recordID INT UNSIGNED AUTO_INCREMENT,
            bossID INT UNSIGNED,
            playerID VARCHAR(20),
            damage INT UNSIGNED,
            isFull BOOLEAN,
            PRIMARY KEY (recordID));
            '''
        )[0]

        return status



    def resetDatabase(self, auth) -> bool:
        if self.getPermission(auth) < 3:
            return False

        try:
            for i in ['user', 'boss', 'current', 'battle']:
                self.executeDatabaseQuery('DROP TABLE %s;' % (i))
            return True
        except:
            return False


    def executeDatabaseQuery(self, command) -> typing.Tuple[bool, typing.List]:
        retry = 0
        maxRetries = 3

        while retry < maxRetries:
            try:
                cursor = self.databaseConnection.cursor()
                cursor.execute(command)
                self.databaseConnection.commit()
                data = cursor.fetchall() if command.split()[0] == 'SELECT' else []
                cursor.close()
                return True, data
            except mysql.connector.Error as err:
                print(err)
                try:
                    self.databaseConnection.rollback()
                    self.establishDatabaseConnection()
                except:
                    pass

                retry += 1

        return False, []


    def getPermission(self, ID) -> int:
        status, data = self.executeDatabaseQuery(
            'SELECT count(1) WHERE EXISTS (SELECT * FROM user);'
        )
        if data[0][0] == 0:
            return 3
        status, data = self.executeDatabaseQuery(
            '''
            SELECT permission FROM user WHERE userID = '%s';
            ''' % ID
        )
        return data[0][0]


    def setBossHP(self, data, auth) -> bool:
        if self.getPermission(auth) < 3:
            return False

        self.executeDatabaseQuery('TRUNCATE boss;')
        self.executeDatabaseQuery('TRUNCATE current;')

        status = True

        for i in data.keys():
            for k, v in enumerate(data[i]):
                status = status and isinstance(v, int)

                status = status and self.executeDatabaseQuery(
                    '''
                    INSERT INTO boss
                    (bossID, bossStage, bossHP)
                    VALUES
                    (%d, %d, %d);
                    ''' % (i, k + 1, v)
                )[0]

            status = status and self.executeDatabaseQuery(
                '''
                INSERT INTO current
                (bossID, bossStage, bossHP)
                VALUES
                (%d, %d, %d);
                ''' % (i, 1, data[i][0])
            )[0]

        return status


    def dayStarts(self) -> bool:
        return self.executeDatabaseQuery(
            '''
            UPDATE user
            SET daily = 3, scrap = 0, hanging = FALSE;
            '''
        )[0]


    def getBossStatus(self, auth) -> typing.Dict[int, typing.Tuple[int, int]]:
        if self.getPermission(auth) < 2:
            return False

        status, data = self.executeDatabaseQuery('SELECT * FROM current;')
        ret = {}
        if status:
            for i in data:
                ret[i[0]] = (i[1], i[2])
        return ret


    def getPlayerStatus(self, auth) -> typing.Dict[str, typing.Tuple[int, int]]:
        if self.getPermission(auth) < 1:
            return False

        status, data = self.executeDatabaseQuery('SELECT * FROM user;')
        ret = {}
        if status:
            for i in data:
                ret[i[0]] = (i[2], i[3])
        return ret


    def addPlayer(self, ID, permission, auth) -> bool:
        if self.getPermission(auth) < 2:
            return False

        return self.executeDatabaseQuery(
            '''
            INSERT IGNORE INTO user
            (userID, permission, daily, scrap, hanging)
            VALUES
            ('%s', %d, 3, 0, FALSE);
            ''' % (ID, permission)
        )[0]


    def enterBattle(self, playerID, bossID) -> bool:
        if self.getPermission(playerID) < 1:
            return False

        return self.executeDatabaseQuery(
            '''
            INSERT INTO battle
            (bossID, playerID)
            VALUES
            (%d, '%s');
            ''' % (bossID, playerID)
        )[0]


    def cancelBattle(self, playerID) -> bool:
        if self.getPermission(playerID) < 1:
            return False

        return self.executeDatabaseQuery(
            '''
            DELETE FROM battle WHERE playerID = '%s';
            ''' % (playerID)
        )[0]


    def reportDamage(self, bossID, playerID, isFull, damage) -> bool:
        if self.getPermission(playerID) < 1:
            return False

        status = self.executeDatabaseQuery(
            '''
            INSERT INTO record
            (bossID, playerID, isFull, damage)
            VALUES
            (%d, '%s', %s, %d);
            ''' % (bossID, playerID, 'TRUE' if isFull else 'FALSE', damage)
        )[0]

        if isFull:
            status = status and self.executeDatabaseQuery(
                '''
                UPDATE user
                SET daily = daily - 1
                WHERE userID = '%s';
                ''' % (playerID)
            )[0]
        else:
            status = status and self.executeDatabaseQuery(
                '''
                UPDATE user
                SET daily = daily - 1, scrap = scrap + 1
                WHERE userID = '%s';
                ''' % (playerID)
            )[0]

        _, data = self.executeDatabaseQuery('SELECT * FROM current;')
        minStage = 10
        currentStage = 0
        currentHP = 0
        newStage = 0

        for i in data:
            minStage = min(minStage, i[1])
            if i[0] == bossID:
                currentStage = i[1]
                currentHP = i[2]

        if currentHP > damage:
            status = status and self.executeDatabaseQuery(
                '''
                UPDATE current
                SET bossHP = %d
                WHERE bossID = %d;
                ''' % (currentHP - damage, bossID)
            )[0]
            return status

        if not currentStage == minStage:
            status = status and self.executeDatabaseQuery(
                '''
                UPDATE current
                SET bossHP = 0
                WHERE bossID = %d;
                ''' % (bossID)
            )[0]
            return status

        currentStage += 1
        if currentStage <= 3:
            newStage = 1
        elif currentStage <= 10:
            newStage = 2
        elif currentStage <= 30:
            newStage = 3
        elif currentStage <= 40:
            newStage = 4
        else:
            newStage = 5

        _, data = self.executeDatabaseQuery(
            '''
            SELECT bossHP FROM boss
            WHERE bossID = %d AND bossStage = %d;
            ''' % (bossID, newStage)
        )

        status = status and self.executeDatabaseQuery(
            '''
            UPDATE current
            SET bossHP = %d, bossStage = %d
            WHERE bossID = %d;
            ''' % (data[0][0], currentStage, bossID)
        )[0]

        _, data = self.executeDatabaseQuery('SELECT * FROM current;')
        for i in data:
            if i[1] == currentStage - 1 and i[2] == 0:
                _, data = self.executeDatabaseQuery(
                '''
                SELECT bossHP FROM boss
                WHERE bossID = %d AND bossStage = %d;
                ''' % (i[0], newStage)
                )
                status = status and self.executeDatabaseQuery(
                    '''
                    UPDATE current
                    SET bossHP = %d, bossStage = %d
                    WHERE bossID = %d;
                    ''' % (data[0][0], currentStage, i[0])
                )[0]
        return status