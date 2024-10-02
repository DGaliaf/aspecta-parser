import utils.osUtils as osUtils
from config import getConfig


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
        cfg.get("outputDatabase").get("files").get("notEligible"),
        cfg.get("outputDatabase").get("files").get("wallets")
    ]
    if not osUtils.check_files(outputDatabaseDir, outputDatabaseFiles):
        osUtils.create_files(outputDatabaseDir, outputDatabaseFiles)


def initBalancesFolders(cfg: dict):
    balancesDatabaseDir = cfg.get("balancesDatabase").get("dirPath")
    if not osUtils.check_directory(balancesDatabaseDir):
        osUtils.create_directory(balancesDatabaseDir)

    balancesDatabaseFiles = [
        cfg.get("balancesDatabase").get("files").get("balances"),
        cfg.get("balancesDatabase").get("files").get("0_400"),
        cfg.get("balancesDatabase").get("files").get("401_1000"),
        cfg.get("balancesDatabase").get("files").get("1001_plus")
    ]
    if not osUtils.check_files(balancesDatabaseDir, balancesDatabaseFiles):
        osUtils.create_files(balancesDatabaseDir, balancesDatabaseFiles)


def initFolders(cfg: dict) -> None:
    initUserFolders(cfg)
    # --------------------------------------------------------------
    initOutputFolders(cfg)
    # --------------------------------------------------------------
    initBalancesFolders(cfg)
    # --------------------------------------------------------------


if __name__ == "__main__":
    initFolders(getConfig())
