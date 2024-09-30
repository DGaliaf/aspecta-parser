import aiofiles


def readFile(directory: str, filePath: str) -> list[str]:
    with open(directory + filePath, 'r', encoding='utf-8') as file:
        return file.readlines()


def writeToFile(directory: str, filePath: str, text: str) -> None:
    with open(directory + filePath, 'a', encoding='utf-8') as file:
        file.write(text + '\n')


def deleteLine(directory: str, filePath: str, lineToDelete: str) -> None:
    lines = readFile(directory, filePath)
    with open(directory + filePath, 'w', encoding='utf-8') as file:
        for line in lines:
            if line.strip() != lineToDelete:
                file.write(line)


def isLineInFile(directory: str, filePath: str, lineToCheck: str) -> bool:
    lines = readFile(directory, filePath)
    return any(line.strip() == lineToCheck for line in lines)


async def readFileAsync(directory: str, filePath: str) -> list[str]:
    async with aiofiles.open(directory + filePath, 'r', encoding='utf-8') as file:
        return await file.readlines()


async def writeToFileAsync(directory: str, filePath: str, text: str) -> None:
    async with aiofiles.open(directory + filePath, 'a', encoding='utf-8') as file:
        await file.write(text + '\n')


async def deleteLineAsync(directory: str, filePath: str, lineToDelete: str) -> None:
    lines = await readFileAsync(directory, filePath)
    async with aiofiles.open(directory + filePath, 'w', encoding='utf-8') as file:
        for line in lines:
            if line.strip() != lineToDelete:
                await file.write(line)


async def isLineInFileAsync(directory: str, filePath: str, lineToCheck: str) -> bool:
    lines = await readFileAsync(directory, filePath)
    return any(line.strip() == lineToCheck for line in lines)
