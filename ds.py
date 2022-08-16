#Импорт библиотек
import discord
from discord.ext import commands
import secrets
import string
from time import ctime

intents = discord.Intents.default() #Настраиваем чтение участников канала
intents.members = True #Настраиваем чтение участников канала

client=commands.Bot(intents=intents, command_prefix = '$') #Выдаем префикс боту
today = str(ctime()) #Переменная с актуальной датой
link1="https://" #Ссылка на чит
link2="https://"
password="смотрите в инструкции" #Пароль от архива с читом
ukey = '' #Индивидуальный ключ активации чита
client.remove_command('help') #удаляем стандартную команду help
users={

} #Буфер базы данных, тут хранятся ключи активации, привязанные к никам

logs = open('log.txt', 'a') #Файл с логами, если его нет - он создается
users_q = open('users.txt', 'a') #Файл с количеством пользователей, именами пользователей и их ключами активации. 

with open('users.txt', 'r', encoding='utf-8') as file:
    num_of_users = int(file.readlines()[0])

with open('users.txt', 'r', encoding='utf-8') as file: #открывам базу данных и записываем пользователей в буфер
    data = file.readlines()[1:]
    for i in range(len(data)):
        nt = data[i].split(sep=' ')
        users[nt[0]]=nt[1][:-1]

try:
    num_of_users=int(data[0]) #получаем количество пользователей для изменения
except:
    pass
    # users_q.write('0') #если файл создался только что, мы начинаем отчет пользователей с 0, т.е. в начале файла пишем количество пользователей, написавших команду >get_cheat

def logwrite(ctx, inf): #функция записи логов
    logs = open('log.txt', 'a', encoding='utf-8')
    try:
        logs.write(f'\n{today} User: {str(ctx.author.name)}#{str(ctx.author.discriminator)} - {inf}') #записываем инфу в логи
    except:
        logs.write(f'\n{today} User: null#{str(ctx.author.discriminator)} - {inf}') #записываем инфу в логи, если ник не стандартный
    logs.close()

def check(st): #функция проверки на наличие ника в базе данных
    with open('users.txt', 'r') as datafile:
        for line in datafile:
            str_list = line.split(sep=' ')
            if str(st) == str(str_list[0]):
                return True
                break
    return False

def rand_str(length): #функция сосдания строки из рандомных символов, где length - длина строки
            letters_and_digits = string.ascii_letters + string.digits
            crypt_rand_string = ''.join(secrets.choice(
                letters_and_digits) for i in range(length))
            return(crypt_rand_string)

@client.command(aliases = ['help']) #Список команд
async def hlps(ctx):
    embed = discord.Embed(colour=ctx.author.color,timestamp=ctx.message.created_at)
    embed.add_field(name='$get_cheat',value='Получить ссылку на чит', inline=False),
    embed.add_field(name='$whois (@user)',value='Получение информации о пользователе', inline=False),
    embed.add_field(name='$userlist (ADMINS ONLY)',value='Список пользователей', inline=False),
    embed.add_field(name='$clear №  (ADMINS ONLY)',value='Удаляем № сообщений', inline=False),
    embed.add_field(name='$info',value='Информация о чите', inline=False)
    await ctx.send(embed=embed)

@client.event
async def on_message(message): #Функция фильтрации чата
    banwords = ["вирус", "ратник", "rat"] #запрещенные слова
    for word in banwords:
        if word in message.content.lower():
            await message.delete() #удаляем сообщение
            await message.author.kick() #кикаем пользователя, написавшего это сообщение
            logwrite(message, str('was kicked from server'))
    await client.process_commands(message) #после проверки продолжаем выполнять код

@client.event
async def on_ready():#надпись в консоль об активации бота
    print(ctime()+': Bot activated') 

@client.command(aliases = ['ping']) #функция проверки бота. Вы пишете ping, он отвечает понг
async def pp(ctx):
    await ctx.send("Pong!") #Отправить сообщение "Pong!" в чат

@client.command(aliases = ['get_cheat']) #функция выдачи чита
async def gc(ctx):
    global num_of_users
    global ukey
    if check(str(ctx.author.name)) or ctx.author.name in users: #проверка на наличие имени в базе данных
        with open('users.txt', 'r', encoding='utf-8') as datafile:
            for line in datafile:
                str_list = line.split(sep=' ')
                if str(ctx.author.name) == str(str_list[0]):
                    ukey = str_list[1] #Если пользователь нашелся, то у него уже есть ключ активации
    else:
        ukey = str(rand_str(16)) #сгенерированный код активации для нового пользователя
        logwrite(ctx, str('got a cheat'))
        users_q = open('users.txt', 'a', encoding='utf-8')
        users_q.write(f'\n{str(ctx.author.name)} {str(ukey)}') #сохраняем имя пользователя и его ключ в базу даннных
        users_q.close()
        with open ('users.txt', 'r', encoding='utf-8') as tx: #открываем базу данных
            old_data = tx.read()
        new_data = old_data.replace(str(num_of_users), str(num_of_users+1)) #заменяем старое значение количества пользователей на +1
        with open ('users.txt', 'w', encoding='utf-8') as tx: #обновляем файл
            tx.write(new_data)
        users[ctx.author.name]=ukey #добавляем ключ пользователя в буфер базы данных
        num_of_users+=1
    text = f'''Ссылка на скачивание: {link1}
        -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
        Зеркало: {link2}
        -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
        Код активации чита: {ukey}
        -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
        Пароль от архива: {password}
        -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
        Обновление от 25 апреля 2022 года (non detected)
        -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
        Количество пользователей: {str(num_of_users+3147)}
        -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=''' #генерируем такой текст (все переменные см. ранее)
    await ctx.author.send(text) #отправляем сгенерированный тест пользователю в лс
    await ctx.send("Чит отправлен в личные сообщения!") #отчет об отправке
    
@client.command(aliases = ['whois']) #Функция проверки пользователя
async def who(ctx, user:discord.Member=None):
    if user == None:
        user=ctx.author #если пользователь не ввел ничье имя, то проверяем автора сообщения
    #Генерируем сообщение с инфой о пользователе
    embed = discord.Embed(colour=user.color,timestamp=ctx.message.created_at)
    embed.set_author(name=f"User info - {user}"),
    embed.set_thumbnail(url=user.avatar_url),
    embed.add_field(name='ID: ', value=str(user.id)+"#"+str(user.discriminator), inline=False)
    embed.add_field(name='Name: ', value=user.display_name, inline=False)
    embed.add_field(name='Created at: ', value=user.created_at, inline=False)
    embed.add_field(name='Joined at: ', value=user.joined_at, inline=False)
    embed.add_field(name='Top role: ', value=user.top_role.mention, inline=False)
    #Отправляем сгенерированное сообщение
    await ctx.send(embed=embed)
    logwrite(ctx, str(f'check {user}'))

@client.command(aliases = ['userlist']) #Функция вывода базы данных
async def ul(ctx):
    if str(ctx.author.top_role) == 'ADMIN': #Проверка на роль, так как могут выводить только админы
        embed = discord.Embed(colour=ctx.author.color,timestamp=ctx.message.created_at) #Генерируем сообщение
        uslist = open('users.txt', 'r', encoding='utf-8') #Открываем базу данных
        k=0 #Счетчик
        for line in uslist: #Перебор строк базы данных
            if k == 0: #В первой строке количество пользователей
                embed.add_field(name="Количество пользователей в БД: ", value=str(line), inline=False)
                k+=1
            else: #В остальных строках выводим имя пользователя и его ключ
                str_list = line.split(sep=' ')
                embed.add_field(name=str(k)+". "+str(str_list[0]), value="Ключ: "+str(str_list[1]), inline=False)
                k+=1
        await ctx.send(embed=embed) #Отправляем сообщение
        logwrite(ctx, str('print userlist'))
    else:
        await ctx.send("У вас недостаточно прав!")

@client.command(aliases = ['clear']) #Функция удаления сообщений
async def delt(ctx, num):
    if str(ctx.author.top_role) == 'ADMIN':
        await ctx.channel.purge(limit=int(num)+1)
        logwrite(ctx, str(f'delete {num} message'))
    else:
        await ctx.send("У вас недостаточно прав!")

@client.command(aliases = ['info']) #Функция вывода рекламы чита
async def inf(ctx):
    embed = discord.Embed(colour=ctx.author.color,timestamp=ctx.message.created_at)
    embed.add_field(name="Информация о чите", value="Читы на CS:GO — это запрещенные программы которые дают значительное преимущество в игре Counter-Strike: Global Offensive. За использование неактуальных читов в 2022 вы можете быть забанены VAC", inline=False)
    embed.add_field(name="Описание", value="Новый бесплатный и рабочий HVH чит для игры CSGO с конфигами. Это отличный способ сыграть против других читеров на серверах hvh, таких как arena или любых других публичных серверах. Если вам нравится играть против других читеров, используя читы, то мы советуем вам использовать этот новый бесплатный чит HVH.", inline=False)
    await ctx.author.send(embed=embed)
    await ctx.send("Информация отправлена в личные сообщения!") #отчет об отправке
    logwrite(ctx, 'get info about cheat')

@client.command(aliases = ['sar']) #Функция отправки рекламы в лс всем, кто на сервере
async def members(ctx):
    embed = discord.Embed(colour=ctx.author.color,timestamp=ctx.message.created_at)
    embed.add_field(name="Обновление! (version 5.4.16)", value="Вышла наиболее актуальная версия чита! Для получения ссылки на загрузку, зайдите в наш канал и напишите $get_cheat", inline=False)
    for Every_Member in ctx.guild.members:
        if Every_Member.bot != True:
            await Every_Member.send(embed=embed)
    logwrite(ctx, 'send a add')

# @client.command(aliases = ['Отправь_правила']) #Функция вывода рекламы чита
# async def rules(ctx):
#     embed = discord.Embed(colour=ctx.author.color,timestamp=ctx.message.created_at)
#     embed.add_field(name="1. Администратор всегда прав", value="Наказание за нарушение: МУТ", inline=False)
#     embed.add_field(name="2. Общение на данном сервере разрешено на русском и английском языках", value="Наказание за нарушение: МУТ", inline=False)
#     embed.add_field(name="3. Не выпрашивайте какие-либо роли или что-то еще", value="Наказание за нарушение: МУТ", inline=False)
#     embed.add_field(name="4. Запрещена дискриминация/унижение пользователей по любому признаку", value="Наказание за нарушение: КИК", inline=False)
#     embed.add_field(name="5. Реклама чего-либо на данном сервере без согласования с администрацией запрещена", value="Наказание за нарушение: КИК", inline=False)
#     embed.add_field(name="6. Запрещено оскорбление администрации", value="Наказание за нарушение: БАН", inline=False)
#     embed.add_field(name="7. Любые заявление порочащие репутацию администрации/проекта без каких-либо весомых доказательств запрещены", value="Наказание за нарушение: КИК", inline=False)
#     embed.add_field(name="8. Запрещено использовать программы для изменения голоса и тд", value="Наказание за нарушение: МУТ", inline=False)
#     embed.add_field(name="9. Администрация имеет право применить любые меры воздействия к вашему аккаунту без объяснения причин", value="Наказание за нарушение: по ситуации", inline=False)
#     await ctx.send(embed=embed)

# @client.command(aliases = ['У_нас_новость']) #Функция вывода рекламы чита
# async def news(ctx):
#     await ctx.send("@everyone")
#     embed = discord.Embed(colour=ctx.author.color,timestamp=ctx.message.created_at)
#     embed.add_field(name="Новость!", value="Наш бот официально запущен! Для получения подробной информации напишите в чате $help!", inline=False)
#     await ctx.send(embed=embed)


client.run(" ") #Токен бота
