#!/usr/bin/env bash

# ==============================================================================
# 🌌 DarkMatterK3@Home Service & Tunnel Manager (Codename: NEON K3)
# ==============================================================================
# This script manages the background services (Streamlit Dashboard and Physics
# Worker) and provides tunneling solutions to access the dashboard securely
# even after closing the SSH session.
# ==============================================================================

set -euo pipefail

# --- CONFIGURATION ---
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STREAMLIT_APP="$SCRIPT_DIR/app_darkmatter.py"
WORKER_APP="$SCRIPT_DIR/real_euclid_worker.py"
TMUX_SESSION="darkmatter"
PORT=8501
LOG_DIR="$SCRIPT_DIR/logs"
PID_DIR="$SCRIPT_DIR/.pids"

# --- COLOR PALETTE (Cyberpunk Theme) ---
CYAN='\033[0;36m'
GOLD='\033[0;33m'
GREEN='\033[0;32m'
RED='\033[0;31m'
PURPLE='\033[0;35m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color
BOLD='\033[1m'

# --- INITIALIZATION ---
mkdir -p "$LOG_DIR"
mkdir -p "$PID_DIR"

# Print Header
print_header() {
    echo -e "${CYAN}==============================================================================${NC}"
    echo -e "${GOLD}${BOLD}             🌌 DarkMatterK3@Home — SERVICE & TUNNEL MANAGER${NC}"
    echo -e "${CYAN}==============================================================================${NC}"
}

# Print Usage
show_help() {
    print_header
    echo -e "Usage: ${BOLD}./manage_darkmatter.sh${NC} [COMMAND]"
    echo ""
    echo -e "${BOLD}Commands:${NC}"
    echo -e "  ${GREEN}start${NC}       Start the Streamlit dashboard & physics worker in the background (tmux)."
    echo -e "  ${RED}stop${NC}        Stop all running services and active tunnels."
    echo -e "  ${GOLD}status${NC}      Check if services and tunnels are running."
    echo -e "  ${BLUE}restart${NC}     Restart all services."
    echo -e "  ${PURPLE}logs${NC}        View live log outputs."
    echo -e "  ${CYAN}attach${NC}      Attach to the active tmux session (interactive terminal monitoring)."
    echo -e "  ${GREEN}tunnel${NC}      Configure/start a public tunnel or display local forwarding instructions."
    echo -e "  ${BOLD}help${NC}        Show this help message."
    echo ""
    echo -e "${BOLD}Note:${NC} By using ${GOLD}tmux${NC}, all processes survive SSH disconnection automatically!"
    echo -e "      You can disconnect safely anytime and reconnect to check progress."
    echo -e "${CYAN}==============================================================================${NC}"
}

# Check if tmux is installed
check_tmux() {
    if ! command -v tmux &> /dev/null; then
        echo -e "${RED}[WARNING] tmux is not installed.${NC} Standard 'nohup' background running will be used as a fallback."
        echo -e "To install tmux for a better experience, run: ${BOLD}sudo apt-get install tmux${NC}"
        return 1
    fi
    return 0
}

# Check if port is in use
is_port_busy() {
    local port=$1
    if command -v ss &> /dev/null; then
        ss -tuln | grep -q ":$port "
    elif command -v netstat &> /dev/null; then
        netstat -tuln | grep -q ":$port "
    elif command -v lsof &> /dev/null; then
        lsof -i :"$port" &> /dev/null
    else
        # Fallback if no network tools are available
        return 1
    fi
}

# Start Services
start_services() {
    print_header
    
    # 1. Check if already running
    if check_tmux && tmux has-session -t "$TMUX_SESSION" 2>/dev/null; then
        echo -e "${GOLD}[INFO] A tmux session '${TMUX_SESSION}' is already running.${NC}"
        echo -e "Use ${BOLD}./manage_darkmatter.sh attach${NC} to view it, or ${RED}./manage_darkmatter.sh stop${NC} to stop it."
        exit 0
    fi
    
    if is_port_busy "$PORT"; then
        echo -e "${RED}[ERROR] Port $PORT is already in use!${NC}"
        echo -e "Please stop any process running on port $PORT and try again."
        exit 1
    fi

    echo -e "${CYAN}[1/3] Starting Streamlit Dashboard...${NC}"
    
    if check_tmux; then
        # Create detached tmux session for the Dashboard
        tmux new-session -d -s "$TMUX_SESSION" -n "Dashboard" "streamlit run \"$STREAMLIT_APP\" --server.port $PORT --server.address 0.0.0.0 2>&1 | tee \"$LOG_DIR/streamlit.log\""
        
        echo -e "${CYAN}[2/3] Starting Physics Worker (real_euclid_worker.py)...${NC}"
        # Add a new window for the background worker (unbuffered for live logging)
        tmux new-window -t "$TMUX_SESSION" -n "Worker" "python3 -u \"$WORKER_APP\" 2>&1 | tee \"$LOG_DIR/worker.log\""
        
        echo -e "${GREEN}[3/3] Services started successfully inside tmux!${NC}"
        echo -e ""
        echo -e "👉 Your processes are now completely isolated from your SSH session."
        echo -e "👉 You can safely close your terminal or lose SSH connection."
        echo -e "👉 To inspect the running processes interactively, run: ${BOLD}./manage_darkmatter.sh attach${NC}"
        echo -e "👉 To set up a tunnel to access the UI, run: ${BOLD}./manage_darkmatter.sh tunnel${NC}"
    else
        # Nohup fallback
        echo -e "${GOLD}[FALLBACK] Starting services with nohup...${NC}"
        
        nohup streamlit run "$STREAMLIT_APP" --server.port $PORT --server.address 0.0.0.0 > "$LOG_DIR/streamlit.log" 2>&1 &
        echo $! > "$PID_DIR/streamlit.pid"
        
        nohup python3 -u "$WORKER_APP" > "$LOG_DIR/worker.log" 2>&1 &
        echo $! > "$PID_DIR/worker.pid"
        
        echo -e "${GREEN}Services started in background using nohup.${NC}"
        echo -e "Log files are located in ${BOLD}$LOG_DIR/${NC}"
    fi
}

# Stop Services
stop_services() {
    print_header
    echo -e "${RED}Stopping all services and tunnels...${NC}"
    
    # 1. Stop tmux session
    if check_tmux && tmux has-session -t "$TMUX_SESSION" 2>/dev/null; then
        tmux kill-session -t "$TMUX_SESSION"
        echo -e "${GREEN}✓ Terminated tmux session '${TMUX_SESSION}'.${NC}"
    fi
    
    # 2. Stop fallback nohup processes if they exist
    if [ -f "$PID_DIR/streamlit.pid" ]; then
        local pid
        pid=$(cat "$PID_DIR/streamlit.pid")
        if kill -0 "$pid" 2>/dev/null; then
            kill "$pid" || kill -9 "$pid"
            echo -e "${GREEN}✓ Stopped Streamlit (PID $pid).${NC}"
        fi
        rm -f "$PID_DIR/streamlit.pid"
    fi
    
    if [ -f "$PID_DIR/worker.pid" ]; then
        local pid
        pid=$(cat "$PID_DIR/worker.pid")
        if kill -0 "$pid" 2>/dev/null; then
            kill "$pid" || kill -9 "$pid"
            echo -e "${GREEN}✓ Stopped Worker (PID $pid).${NC}"
        fi
        rm -f "$PID_DIR/worker.pid"
    fi
    
    # Kill any dangling localtunnel or other ssh tunnel launched by this script
    pkill -f "localhost.run" || true
    pkill -f "serveo.net" || true
    pkill -f "streamlit run" || true
    pkill -f "real_euclid_worker.py" || true
    
    echo -e "${GREEN}All services successfully stopped.${NC}"
}

# Status Check
check_status() {
    print_header
    local active=0
    
    if check_tmux && tmux has-session -t "$TMUX_SESSION" 2>/dev/null; then
        echo -e "Tmux session '${TMUX_SESSION}': ${GREEN}${BOLD}RUNNING${NC}"
        echo -e "Active windows in tmux:"
        tmux list-windows -t "$TMUX_SESSION" -F "  - #I: #W (#F)"
        active=1
    else
        echo -e "Tmux session '${TMUX_SESSION}': ${RED}STOPPED${NC}"
    fi
    
    # Check if port 8501 is active
    if is_port_busy "$PORT"; then
        echo -e "Streamlit Dashboard (Port $PORT): ${GREEN}${BOLD}LISTENING${NC}"
        active=1
    else
        echo -e "Streamlit Dashboard (Port $PORT): ${RED}NOT LISTENING${NC}"
    fi
    
    # Check if worker is running (by process search)
    if pgrep -f "real_euclid_worker.py" > /dev/null; then
        echo -e "Physics Worker (real_euclid_worker.py): ${GREEN}${BOLD}RUNNING${NC}"
        active=1
    else
        echo -e "Physics Worker (real_euclid_worker.py): ${RED}STOPPED${NC}"
    fi
    
    # Check for active public tunnels
    if pgrep -f "localhost.run" > /dev/null || pgrep -f "serveo.net" > /dev/null; then
        echo -e "Public Tunnel: ${GREEN}${BOLD}ACTIVE${NC}"
        if [ -f "$LOG_DIR/tunnel.log" ]; then
            echo -e "Tunnel URL details:"
            grep -E "https://[a-zA-Z0-9.-]+\.(localhost\.run|serveo\.net)" "$LOG_DIR/tunnel.log" | tail -n 2 || true
        fi
    else
        echo -e "Public Tunnel: ${RED}INACTIVE${NC}"
    fi
    
    if [ $active -eq 0 ]; then
        echo ""
        echo -e "${GOLD}No active DarkMatterK3@Home services are currently running.${NC}"
        echo -e "Run ${BOLD}./manage_darkmatter.sh start${NC} to boot up the system."
    fi
}

# Attach to tmux
attach_tmux() {
    if check_tmux; then
        if tmux has-session -t "$TMUX_SESSION" 2>/dev/null; then
            echo -e "${GREEN}Attaching to tmux session '${TMUX_SESSION}'...${NC}"
            echo -e "${GOLD}To detach from this session without stopping the servers, press: ${BOLD}Ctrl + B, then D${NC}"
            sleep 2
            tmux attach-session -t "$TMUX_SESSION"
        else
            echo -e "${RED}[ERROR] No active tmux session found.${NC}"
            echo -e "Start services first using: ${BOLD}./manage_darkmatter.sh start${NC}"
        fi
    else
        echo -e "${RED}[ERROR] Cannot attach: tmux is not available on this system.${NC}"
    fi
}

# Show logs
view_logs() {
    print_header
    echo -e "Choose log file to view:"
    echo -e "  ${CYAN}1)${NC} Streamlit Dashboard Log"
    echo -e "  ${CYAN}2)${NC} Physics Worker Log"
    echo -e "  ${CYAN}3)${NC} Tunnel Log (if active)"
    echo -e "  ${CYAN}4)${NC} Exit"
    read -rp "Select option (1-4): " opt
    
    case $opt in
        1)
            if [ -f "$LOG_DIR/streamlit.log" ]; then
                tail -n 100 -f "$LOG_DIR/streamlit.log"
            else
                echo -e "${RED}No Streamlit log file found at $LOG_DIR/streamlit.log${NC}"
            fi
            ;;
        2)
            if [ -f "$LOG_DIR/worker.log" ]; then
                tail -n 100 -f "$LOG_DIR/worker.log"
            else
                echo -e "${RED}No Worker log file found at $LOG_DIR/worker.log${NC}"
            fi
            ;;
        3)
            if [ -f "$LOG_DIR/tunnel.log" ]; then
                tail -n 100 -f "$LOG_DIR/tunnel.log"
            else
                echo -e "${RED}No Tunnel log file found at $LOG_DIR/tunnel.log${NC}"
            fi
            ;;
        *)
            echo "Exiting logs."
            ;;
    esac
}

# Manage Tunneling
manage_tunnel() {
    print_header
    
    # Auto-detect public IP of the host
    local public_ip
    public_ip=$(curl -s https://ifconfig.me || curl -s https://api.ipify.org || echo "YOUR_SERVER_IP")
    local username
    username=$(whoami)
    
    echo -e "${BOLD}Select a Tunneling Method to Access your Streamlit App remotely:${NC}"
    echo ""
    echo -e "  ${CYAN}Method 1: Secure SSH Local Port Forwarding (Recommended)${NC}"
    echo -e "    Keep the server completely private. Run this command on your ${GOLD}LOCAL MACHINE${NC}:"
    echo -e "    ${BOLD}ssh -N -L $PORT:localhost:$PORT ${username}@${public_ip}${NC}"
    echo -e "    Then open your browser and navigate to: ${GREEN}http://localhost:$PORT${NC}"
    echo ""
    echo -e "  ${CYAN}Method 2: Zero-Config Public HTTPS Tunnel (localhost.run)${NC}"
    echo -e "    Exposes your app to a public HTTPS URL without installing any software."
    echo -e "    Runs completely over secure outbound SSH. Excellent for instant access."
    echo ""
    echo -e "  ${CYAN}Method 3: Zero-Config Public HTTPS Tunnel (serveo.net)${NC}"
    echo -e "    Alternative secure SSH public tunnel."
    echo ""
    echo -e "  ${CYAN}Method 4: View active tunnel URL / Log${NC}"
    echo -e "  ${CYAN}Method 5: Close active tunnels${NC}"
    echo -e "  ${CYAN}Method 6: Back to main menu${NC}"
    echo ""
    read -rp "Select option (1-6): " tunnel_opt
    
    case $tunnel_opt in
        1)
            echo -e "${GREEN}Method 1 selected.${NC}"
            echo -e "Please copy the following command and run it in a terminal on your ${BOLD}local computer${NC}:"
            echo -e "\n  ${BOLD}ssh -N -L $PORT:localhost:$PORT ${username}@${public_ip}${NC}\n"
            echo -e "Once executed, keep that terminal open, and open ${GREEN}http://localhost:$PORT${NC} in your local browser."
            ;;
        2)
            echo -e "${GREEN}Launching public tunnel via localhost.run...${NC}"
            if check_tmux; then
                if ! tmux has-session -t "$TMUX_SESSION" 2>/dev/null; then
                    echo -e "${RED}[ERROR] Services must be running first! Run ./manage_darkmatter.sh start${NC}"
                    exit 1
                fi
                
                # Close any existing tunnel window
                tmux kill-window -t "$TMUX_SESSION:Tunnel" 2>/dev/null || true
                
                # Start public tunnel in a new tmux window
                tmux new-window -t "$TMUX_SESSION" -n "Tunnel" "ssh -o StrictHostKeyChecking=no -R 80:localhost:$PORT nokey@localhost.run 2>&1 | tee \"$LOG_DIR/tunnel.log\""
                
                echo -e "${GOLD}Establishing tunnel... (takes 5-10 seconds)${NC}"
                sleep 6
                
                if grep -q "localhost.run" "$LOG_DIR/tunnel.log"; then
                    echo -e "${GREEN}Tunnel successfully created in tmux session!${NC}"
                    echo -e "Your public URL is:"
                    grep -o "https://[a-zA-Z0-9.-]\+\.localhost\.run" "$LOG_DIR/tunnel.log" | head -n 1 || echo -e "${GOLD}Could not parse URL yet. Run Method 4 to check or attach to tmux with 'attach'.${NC}"
                    echo -e ""
                    echo -e "This tunnel runs inside your background tmux session, so ${GREEN}it will survive SSH disconnection!${NC}"
                else
                    echo -e "${RED}Tunnel connection may have failed. Checking log output:${NC}"
                    cat "$LOG_DIR/tunnel.log"
                fi
            else
                echo -e "${RED}[ERROR] Public background tunnels require tmux to survive SSH disconnection.${NC}"
            fi
            ;;
        3)
            echo -e "${GREEN}Launching public tunnel via serveo.net...${NC}"
            if check_tmux; then
                if ! tmux has-session -t "$TMUX_SESSION" 2>/dev/null; then
                    echo -e "${RED}[ERROR] Services must be running first! Run ./manage_darkmatter.sh start${NC}"
                    exit 1
                fi
                
                # Close any existing tunnel window
                tmux kill-window -t "$TMUX_SESSION:Tunnel" 2>/dev/null || true
                
                # Start serveo tunnel in a new tmux window
                tmux new-window -t "$TMUX_SESSION" -n "Tunnel" "ssh -o StrictHostKeyChecking=no -R 80:localhost:$PORT serveo.net 2>&1 | tee \"$LOG_DIR/tunnel.log\""
                
                echo -e "${GOLD}Establishing tunnel... (takes 5-10 seconds)${NC}"
                sleep 6
                
                if grep -q "serveo.net" "$LOG_DIR/tunnel.log"; then
                    echo -e "${GREEN}Tunnel successfully created in tmux session!${NC}"
                    echo -e "Your public URL is:"
                    grep -o "https://[a-zA-Z0-9.-]\+\.serveo\.net" "$LOG_DIR/tunnel.log" | head -n 1 || echo -e "${GOLD}Could not parse URL yet. Run Method 4 to check or attach to tmux with 'attach'.${NC}"
                    echo -e ""
                    echo -e "This tunnel runs inside your background tmux session, so ${GREEN}it will survive SSH disconnection!${NC}"
                else
                    echo -e "${RED}Tunnel connection may have failed. Checking log output:${NC}"
                    cat "$LOG_DIR/tunnel.log"
                fi
            else
                echo -e "${RED}[ERROR] Public background tunnels require tmux to survive SSH disconnection.${NC}"
            fi
            ;;
        4)
            if [ -f "$LOG_DIR/tunnel.log" ]; then
                echo -e "${CYAN}--- Active Tunnel Logs ---${NC}"
                cat "$LOG_DIR/tunnel.log" | tail -n 15
                echo -e "${CYAN}--------------------------${NC}"
                echo -e "Look for a URL ending in ${BOLD}.localhost.run${NC} or ${BOLD}.serveo.net${NC} above."
            else
                echo -e "${RED}No active public tunnel log found.${NC}"
            fi
            ;;
        5)
            echo -e "${RED}Closing active public tunnels...${NC}"
            pkill -f "localhost.run" || true
            pkill -f "serveo.net" || true
            if check_tmux && tmux has-session -t "$TMUX_SESSION" 2>/dev/null; then
                tmux kill-window -t "$TMUX_SESSION:Tunnel" 2>/dev/null || true
            fi
            echo -e "${GREEN}✓ All public tunnels closed.${NC}"
            ;;
        *)
            echo "Returning to main menu."
            ;;
    esac
}

# --- MAIN EXECUTION ---
if [ $# -eq 0 ]; then
    show_help
    exit 0
fi

CMD=$1
case "$CMD" in
    start)
        start_services
        ;;
    stop)
        stop_services
        ;;
    status)
        check_status
        ;;
    restart)
        stop_services
        sleep 2
        start_services
        ;;
    logs)
        view_logs
        ;;
    attach)
        attach_tmux
        ;;
    tunnel)
        manage_tunnel
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo -e "${RED}Unknown command: $CMD${NC}"
        echo ""
        show_help
        exit 1
        ;;
esac
