import utils.osUtils as osUtils


def initUserFolders(cfg: dict):
    userDatabaseDir = cfg.get("usersDatabase").get("dirPath")
    if not osUtils.check_directory(userDatabaseDir):
        osUtils.create_directory(userDatabaseDir)

    userDatabaseFiles = [
        cfg.get("usersDatabase").get("files").get("toParse"),
        cfg.get("usersDatabase").get("files").get("parsed")
    ]
    if not osUtils.check_files(userDatabaseDir, userDatabaseFiles):
        osUtils.create_files(userDatabaseDir, userDatabaseFiles)


def initOutputFolders(cfg: dict):
    outputDatabaseDir = cfg.get("outputDatabase").get("dirPath")
    if not osUtils.check_directory(outputDatabaseDir):
        osUtils.create_directory(outputDatabaseDir)

    outputDatabaseFiles = [
        cfg.get("outputDatabase").get("files").get("eligible"),
        cfg.get("outputDatabase").get("files").get("notEligible")
    ]
    if not osUtils.check_files(outputDatabaseDir, outputDatabaseFiles):
        osUtils.create_files(outputDatabaseDir, outputDatabaseFiles)


def initFolders(cfg: dict) -> None:
    initUserFolders(cfg)
    # --------------------------------------------------------------
    initOutputFolders(cfg)
    # --------------------------------------------------------------
