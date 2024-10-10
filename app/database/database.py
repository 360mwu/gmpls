import aiomysql
import warnings
from data.utils.logger import error_logger

warnings.filterwarnings("ignore", category=aiomysql.Warning)

class Database:
    def __init__(self, host, user, password, db, port, prefix):
        self.host = host
        self.user = user
        self.password = password
        self.db = db
        self.port = port
        self.prefix = prefix
        self.connection = None

    async def connect(self):
        if self.connection is None:
            self.connection = await aiomysql.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                db=self.db
            )

    async def close(self):
        if self.connection:
            await self.connection.ensure_closed()  
            self.connection = None

    async def check_connection(self):
        try:
            await self.connect()
            await self.close()
            return True
        except Exception as e:
            await error_logger(f"Error check connection db as: {e}")
            return False

    async def create_tables(self):
        await self.create_user_access_table()  
        await self.create_servers_table()  
        await self.create_settings_table()  

    async def create_user_access_table(self):
        try:
            await self.connect()
            async with self.connection.cursor() as cursor:
                create_table_query = f"""
                CREATE TABLE IF NOT EXISTS `{self.prefix}user_access` (
                    `id` INT PRIMARY KEY AUTO_INCREMENT,
                    `steamid64` BIGINT NOT NULL UNIQUE,
                    `monitoring` BOOLEAN NOT NULL,
                    `privileges` BOOLEAN NOT NULL,
                    `punishments` BOOLEAN NOT NULL,
                    `control` BOOLEAN NOT NULL
                );
                """
                await cursor.execute(create_table_query)
                await self.connection.commit()
        except Exception as e:
            await error_logger(f"Error creating table {self.prefix}user_access: {e}")
        finally:
            await self.close()

    async def create_servers_table(self):
        try:
            await self.connect()
            async with self.connection.cursor() as cursor:
                create_table_query = f"""
                CREATE TABLE IF NOT EXISTS `{self.prefix}servers` (
                    `id` INT PRIMARY KEY AUTO_INCREMENT,
                    `name_server` VARCHAR(255) NOT NULL,
                    `ip` VARCHAR(255) NOT NULL,
                    `port` INT NOT NULL,
                    `rcon_password` VARCHAR(255) NOT NULL,
                    `iks_host` VARCHAR(255) NOT NULL,
                    `iks_user` VARCHAR(255) NOT NULL,
                    `iks_database` VARCHAR(255) NOT NULL,
                    `iks_password` VARCHAR(255) NOT NULL,
                    `iks_server_id` VARCHAR(255) NOT NULL,
                    `vip_host` VARCHAR(255) NOT NULL,
                    `vip_user` VARCHAR(255) NOT NULL,
                    `vip_database` VARCHAR(255) NOT NULL,
                    `vip_password` VARCHAR(255) NOT NULL,
                    `vip_server_id` INT NOT NULL
                );
                """
                await cursor.execute(create_table_query)
                await self.connection.commit()
        except Exception as e:
            await error_logger(f"Error creating table {self.prefix}servers: {e}")
        finally:
            await self.close()

    async def create_settings_table(self):
        try:
            await self.connect()
            async with self.connection.cursor() as cursor:
                create_table_query = f"""
                CREATE TABLE IF NOT EXISTS `{self.prefix}settings` (
                    `id` INT PRIMARY KEY AUTO_INCREMENT,
                    `vip_type` INT CHECK(vip_type IN (0, 1)),
                    `discord_log` INT CHECK(discord_log IN (0, 1)),
                    `discord_url` VARCHAR(255)
                );
                """
                await cursor.execute(create_table_query)
                await self.connection.commit()

                await cursor.execute(f'SELECT COUNT(*) FROM `{self.prefix}settings`')
                count = await cursor.fetchone()
                
                if count[0] == 0:
                    await cursor.execute(f'''
                        INSERT INTO `{self.prefix}settings` 
                        (vip_type, discord_log, discord_url) 
                        VALUES (0, 0, NULL);
                    ''')
                    await self.connection.commit()

                await cursor.execute(f'''
                    CREATE TRIGGER IF NOT EXISTS `{self.prefix}restrict_insert` 
                    BEFORE INSERT ON `{self.prefix}settings`
                    FOR EACH ROW
                    BEGIN
                        DECLARE msg VARCHAR(255);
                        SET msg = 'Cannot insert new rows into {self.prefix}settings';
                        IF (SELECT COUNT(*) FROM `{self.prefix}settings`) >= 1 THEN
                            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = msg;
                        END IF;
                    END;
                ''')
                await self.connection.commit()

        except Exception as e:
            await error_logger(f"Error creating table {self.prefix}settings: {e}")
        finally:
            await self.close()

