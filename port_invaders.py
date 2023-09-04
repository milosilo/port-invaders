
import pygame
import random
import time
import os

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_SIZE = 50
ENEMY_SIZE = 50
ALLOWED_SIZE = 50
FONT_SIZE = 30
WHITE = (255, 255, 255)

# Function to display text on screen
def display_text(text, pos, screen, font, color=WHITE):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, pos)

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Port Invaders")

# Load font and images
font = pygame.font.SysFont(None, FONT_SIZE)
player_image = pygame.image.load(os.path.join("assets", "player_ship.png"))
enemy_image = pygame.image.load(os.path.join("assets", "enemy_ship.png"))
allowed_image = pygame.image.load(os.path.join("assets", "allowed_ship.png"))
explosion_image = pygame.image.load(os.path.join("assets", "explosion.png"))

# Main game loop
clock = pygame.time.Clock()
level = 1
score = 0
common_ports = [22, 80, 443, 21, 25, 110, 143, 161, 162, 389, 636, 989, 990]

port_names = {
    20: "FTP",
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    465: "SMTPS",
    587: "SMTP",
    993: "IMAPS",
    995: "POP3S",
    3306: "MySQL",
    3389: "RDP",
    5432: "PostgreSQL",
    27017: "MongoDB",
    22: "SFTP",
    161: "SNMP",
    162: "SNMP Trap",
    389: "LDAP",
    636: "LDAPS",
    989: "FTPS Data",
    990: "FTPS Control",
    2049: "NFS",
    3690: "SVN",
    22: "SCP",
    873: "RSYNC",
    6660: "IRC",
    6667: "IRC SSL",
    6697: "IRC SSL",
    9418: "Git",
    1194: "OpenVPN",
    1723: "PPTP",
    5060: "SIP",
    514: "Syslog",
    1080: "SOCKS Proxy",
    3128: "HTTP Proxy",
    8080: "HTTP Proxy",
    8081: "HTTP Proxy",
    21: "FTPS",
    137: "NetBIOS",
    139: "NetBIOS",
    445: "SMB/CIFS",
    514: "Shell",
    135: "MS RPC",
    1433: "MSSQL",
    1521: "Oracle SQL"
}

while True:
    start_time = time.time()
    player_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT - 2 * PLAYER_SIZE]
    allowed_ports = random.sample(common_ports, 3)
    enemies = []
    allowed = []
    bullets = []

    while time.time() - start_time < 15:

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullets.append([player_pos[0] + PLAYER_SIZE // 2, player_pos[1]])

        # Move player
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_pos[0] -= 10
        if keys[pygame.K_RIGHT]:
            player_pos[0] += 10

        # Generate random enemies
        if random.randint(1, 20) == 20:
            enemies.append([random.randint(0, SCREEN_WIDTH - ENEMY_SIZE), 0])

        # Generate allowed ships
        if random.randint(1, 20) == 20:
            allowed.append([random.randint(0, SCREEN_WIDTH - ALLOWED_SIZE), 0, random.choice(allowed_ports)])

        # Update enemy and bullet positions
        for enemy in enemies:
            enemy[1] += 5
            if enemy[1] > SCREEN_HEIGHT:
                enemies.remove(enemy)
                score -= 50

        for bullet in bullets:
            bullet[1] -= 5
            if bullet[1] < 0:
                bullets.remove(bullet)

        # Update allowed positions
        for allow in allowed:
            allow[1] += 5
            if allow[1] > SCREEN_HEIGHT:
                allowed.remove(allow)
                score += 100

        # Collision detection
        for enemy in enemies:
            for bullet in bullets:
                if (
                    bullet[0] > enemy[0]
                    and bullet[0] < enemy[0] + ENEMY_SIZE
                    and bullet[1] > enemy[1]
                    and bullet[1] < enemy[1] + ENEMY_SIZE
                ):
                    bullets.remove(bullet)
                    enemies.remove(enemy)
                    score += 100

        for allow in allowed:
            for bullet in bullets:
                if (
                    bullet[0] > allow[0]
                    and bullet[0] < allow[0] + ALLOWED_SIZE
                    and bullet[1] > allow[1]
                    and bullet[1] < allow[1] + ALLOWED_SIZE
                ):
                    bullets.remove(bullet)
                    allowed.remove(allow)
                    score -= 150

        # Draw everything
        screen.fill((0, 0, 0))

        # Draw player using image
        screen.blit(player_image, (player_pos[0], player_pos[1]))

        # Draw bullets
        for bullet in bullets:
            pygame.draw.circle(screen, WHITE, (bullet[0], bullet[1]), 5)

        # Draw enemies using image
        for enemy in enemies:
            screen.blit(enemy_image, (enemy[0], enemy[1]))

        # Draw allowed using image and display port numbers
        for allow in allowed:
            screen.blit(allowed_image, (allow[0], allow[1]))
            display_text(str(allow[2]), (allow[0] + 10, allow[1] + 55), screen, font, color=(255, 255, 255))

        # Draw score and allowed ports
        display_text(f"Score: {score}", [30, 30], screen, font)
        display_text(f"Allowed Ports: {allowed_ports} - {[port_names[port] for port in allowed_ports]}", [30, 60], screen, font)

        pygame.display.flip()
        clock.tick(30)

    # Level Transition Screen
    screen.fill((0, 0, 0))
    display_text(f"Level {level} Complete!", [250, 250], screen, font)
    display_text(f"Score: {score}", [300, 300], screen, font)
    display_text("Press any key to continue...", [200, 350], screen, font)
    pygame.display.update()
    time.sleep(3)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                break

        if event.type == pygame.KEYDOWN:
            break

    level += 1
    allowed_ports = random.sample(common_ports, 3)
