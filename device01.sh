#!/bin/bash

# Nama sesi tmux
SESSION="device01"

# Perintah untuk layar 1
COMMAND1='unset GITHUB_TOKEN &&'

# Perintah untuk layar 2
COMMAND2='unset GITHUB_TOKEN &&'

# Perintah untuk layar 3
COMMAND3='unset GITHUB_TOKEN &&'

# Perintah untuk layar 4
COMMAND4='unset GITHUB_TOKEN &&'

# Fungsi untuk memeriksa apakah perintah sedang berjalan di layar tertentu
check_command() {
    local pane=$1
    local command=$2
    tmux capture-pane -p -t "$SESSION:$pane" | grep -q "$command"
}

# Jika sesi belum ada, buat sesi dan jalankan perintah
if ! tmux has-session -t $SESSION 2>/dev/null; then
    echo "Sesi '$SESSION' belum ada. Membuat sesi baru..."
    tmux new-session -d -s $SESSION

    # Layar 1
    tmux send-keys -t $SESSION "$COMMAND1" C-m
    echo "Perintah di layar 1 dijalankan. Menunggu 30 detik..."
    sleep 30  # Jeda 30 detik

    # Split layar menjadi dua
    tmux split-window -h -t $SESSION

    # Layar 2
    tmux send-keys -t $SESSION:0.1 "$COMMAND2" C-m
    echo "Perintah di layar 2 dijalankan. Menunggu 30 detik..."
    sleep 30  # Jeda 30 detik

    # Split layar menjadi dua lagi
    tmux split-window -v -t $SESSION

    # Layar 3
    tmux send-keys -t $SESSION:0.2 "$COMMAND3" C-m
    echo "Perintah di layar 3 dijalankan. Menunggu 30 detik..."
    sleep 30  # Jeda 30 detik

    # Split layar menjadi dua lagi
    tmux split-window -v -t $SESSION

    # Layar 4
    tmux send-keys -t $SESSION:0.3 "$COMMAND4" C-m
    echo "Perintah di layar 4 dijalankan."

else
    echo "Sesi '$SESSION' sudah ada. Memeriksa perintah di setiap layar..."
    
    # Layar 1: Jalankan ulang jika perintah tidak ditemukan
    if ! check_command "0.0" "$COMMAND1"; then
        echo "Perintah di layar 1 tidak aktif. Menjalankan ulang..."
        tmux send-keys -t $SESSION:0.0 "$COMMAND1" C-m
        echo "Perintah di layar 1 dijalankan. Menunggu 30 detik..."
        sleep 30  # Jeda 30 detik
    else
        echo "Perintah di layar 1 sudah aktif."
    fi

    # Layar 2: Jalankan ulang jika perintah tidak ditemukan
    if ! check_command "0.1" "$COMMAND2"; then
        echo "Perintah di layar 2 tidak aktif. Menjalankan ulang..."
        tmux send-keys -t $SESSION:0.1 "$COMMAND2" C-m
        echo "Perintah di layar 2 dijalankan. Menunggu 30 detik..."
        sleep 30  # Jeda 30 detik
    else
        echo "Perintah di layar 2 sudah aktif."
    fi

    # Layar 3: Jalankan ulang jika perintah tidak ditemukan
    if ! check_command "0.2" "$COMMAND3"; then
        echo "Perintah di layar 3 tidak aktif. Menjalankan ulang..."
        tmux send-keys -t $SESSION:0.2 "$COMMAND3" C-m
        echo "Perintah di layar 3 dijalankan. Menunggu 30 detik..."
        sleep 30  # Jeda 30 detik
    else
        echo "Perintah di layar 3 sudah aktif."
    fi

    # Layar 4: Jalankan ulang jika perintah tidak ditemukan
    if ! check_command "0.3" "$COMMAND4"; then
        echo "Perintah di layar 4 tidak aktif. Menjalankan ulang..."
        tmux send-keys -t $SESSION:0.3 "$COMMAND4" C-m
        echo "Perintah di layar 4 dijalankan."
    else
        echo "Perintah di layar 4 sudah aktif."
    fi
fi

# Attach ke sesi tmux
tmux attach-session -t $SESSION
