#!/bin/bash

# Скрипт проверки скорости зеркал для Arch Linux
# Использует reflector для тестирования и обновления mirrorlist

LOG_FILE="/var/log/mirror-speed-check.log"
BACKUP_MIRRORLIST="/etc/pacman.d/mirrorlist.backup"
CURRENT_MIRRORLIST="/etc/pacman.d/mirrorlist"

# Функция логирования
log_message() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log_message "Начало проверки скорости зеркал"

# Создаем резервную копию текущего mirrorlist
if [ ! -f "$BACKUP_MIRRORLIST" ]; then
    cp "$CURRENT_MIRRORLIST" "$BACKUP_MIRRORLIST"
    log_message "Создана резервная копия mirrorlist"
fi

# Параметры для reflector
# Вы можете настроить их под свои нужды
COUNTRIES="RU,UA,KZ,BY,GE"  # Предпочтительные страны
PROTOCOL="https"           # Предпочтительный протокол
LATEST="5"                # Брать последние 5 зеркал
SORT="rate"               # Сортировать по скорости

log_message "Проверяем зеркала для стран: $COUNTRIES"

# Запускаем reflector
if command -v reflector &> /dev/null; then
    reflector \
        --country "$COUNTRIES" \
        --protocol "$PROTOCOL" \
        --latest "$LATEST" \
        --sort "$SORT" \
        --save "$CURRENT_MIRRORLIST.tmp" \
        2>&1 | tee -a "$LOG_FILE"
    
    # Проверяем успешность выполнения
    if [ $? -eq 0 ] && [ -s "$CURRENT_MIRRORLIST.tmp" ]; then
        mv "$CURRENT_MIRRORLIST.tmp" "$CURRENT_MIRRORLIST"
        log_message "Mirrorlist успешно обновлен"
        
        # Выводим информацию о новых зеркалах
        log_message "Новый список зеркал:"
        grep -E "^Server" "$CURRENT_MIRRORLIST" | head -5 | tee -a "$LOG_FILE"
    else
        log_message "Ошибка: Не удалось обновить mirrorlist"
        rm -f "$CURRENT_MIRRORLIST.tmp"
    fi
else
    log_message "Ошибка: reflector не установлен"
    log_message "Установите reflector: sudo pacman -S reflector"
fi

log_message "Завершение проверки скорости зеркал"
echo "" >> "$LOG_FILE"
