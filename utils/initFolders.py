import utils.osUtils as osUtils


def initFolders(cfg: dict) -> None:
    userDatabaseDir = cfg.get("usersDatabase").get("dirPath")
    if not osUtils.check_directory(userDatabaseDir):
        osUtils.create_directory(userDatabaseDir)

    userDatabaseFiles = [
        cfg.get("usersDatabase").get("files").get("toParse"),
        cfg.get("usersDatabase").get("files").get("parsed")
    ]
    if not osUtils.check_files(userDatabaseDir, userDatabaseFiles):
        osUtils.create_files(userDatabaseDir, userDatabaseFiles)
