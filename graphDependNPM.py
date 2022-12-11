import requests
from bs4 import BeautifulSoup


def getDependencies(pack):
    packageUrl = f"https://www.npmjs.com/package/{pack}?activeTab=dependencies"
    page = requests.get(packageUrl)
    soup = BeautifulSoup(page.text, "html.parser")
    result = (soup.find_all(string='Dependencies ('))[0].find_parent().find_parent().find_all('ul', {
        'aria-label': 'Dependencies'})[0].find_all('a')
    dependencyList = []
    for depend in result:
        name = depend.text
        dependencyList.append(name)
    return dependencyList


def graphWithDepth(pack, depth, spaces):
    if depth != 1:
        for depend in getDependencies(pack):
            print(spaces + pack + " ➝ " + depend)
            graphWithDepth(depend, depth - 1, spaces + "  ")
    else:
        dependencies = getDependencies(pack)
        for depend in dependencies:
            print(spaces + pack + " ➝ " + depend)
        return


def graph(pack, spaces):
    dependList = getDependencies(pack)
    if len(dependList) != 0:
        for depend in dependList:
            print(spaces + pack + " ➝ " + depend)
            graph(depend, spaces + "  ")
    else:
        for depend in dependList:
            print(spaces + pack + " ➝ " + depend)
        return


print("Имя пакета npm = ", end="")
package = input()
print("Хотите указать глубину погружения? Если да - введите 1, иначе - 0")
print("Ваш ответ: ", end="")
ans = int(input())
if ans == 1:
    print("Глубина погружения = ", end="")
    immersionDepth = int(input())
    if immersionDepth != 0:
        print("\nГраф зависимостей пакета " + package + " с глубиной погружения - " + str(immersionDepth), end="\n\n")
        print("digraph G {")
        graphWithDepth(package, int(immersionDepth), "")
        print("}")
else:
    print("\nГраф зависимостей пакета " + package, end="\n\n")
    print("digraph G {")
    graph(package, "")
    print("}")
