# Umbra

Umbra là game platformer 2D viết bằng Python và Pygame. Người chơi vượt qua các màn chơi băng giá, chiến đấu với quái, boss, mở rương hồi máu và đi qua portal để tới màn tiếp theo.

## Tính năng hiện có

- 3 level, được cấu hình tập trung trong `main.py`.
- Tilemap xuất từ Tiled sang CSV, gồm solid, one-way platform và các layer trang trí.
- Camera cuộn theo cả trục ngang lẫn dọc.
- Player có chạy, nhảy, dash, hai loại tấn công, máu và mạng sống.
- Enemy có tuần tra, phát hiện, đuổi theo và tấn công.
- Boss Ice và Witch; Witch có đòn cận chiến và spell rơi tại vị trí player đã bị khóa.
- Chest hồi máu, checkpoint và portal chuyển level sau boss.
- Menu, pause, restart level, game-over và victory screen.
- Nhạc nền riêng cho menu, gameplay và lúc boss giao chiến.

## Điều khiển

| `A` / `D` | Di chuyển trái / phải |
| `W` / `Space` | Nhảy |
| `U` | Tấn công 1 |
| `I` | Tấn công 2 |
| `J` | Dash |
| `E` | Mở rương hoặc đi qua portal |
| `Esc` | Pause / tiếp tục game |

## Checkpoint và lives

- Mỗi level bắt đầu bằng một spawn point mặc định.
- Khi player chạm checkpoint, vị trí hồi sinh được cập nhật.
- Nếu player chết nhưng vẫn còn lives, game hồi sinh player tại checkpoint gần nhất.
- Restart level đưa player về spawn đầu level và khôi phục số lives tại thời điểm bắt đầu level đó.

## Cấu trúc chính

main.py              # Khởi tạo game, cấu hình level, load map và render
game_states.py       # Menu, playing, pause, game-over, victory
player.py            # Điều khiển, combat và trạng thái player
enemy.py             # AI enemy thường
boss_ice.py          # Ice boss
boss_witch.py        # Witch boss và spell attack
checkpoint.py        # Checkpoint và hồi sinh
chest.py             # Rương hồi máu
portal.py            # Portal chuyển level
audio.py             # Quản lý nhạc nền
ui.py                # HP bar, lives và boss HP bar
tilemap.py           # Đọc CSV, collision và render tile
Map/                 # TMX, CSV level và tileset
graphics/            # Sprite, UI và background
music/               # Menu, gameplay và boss music

## Tạo hoặc sửa level

Level được thiết kế bằng Tiled với tile gốc kích thước `16x16`, sau đó game scale lên `64x64`.

Mỗi level cần các layer CSV sau:

levelN_solid.csv
levelN_oneway.csv
levelN_decorback.csv
levelN_decorfront.csv

Sau khi export từ Tiled, thêm đường dẫn file, vị trí spawn, checkpoint, enemy, boss và chest vào `LEVELS` trong `main.py`.

## Audio

Game dùng ba track:
- `menu.ogg`: phát ở menu.
- `play.ogg`: phát khi khám phá level và sau khi đổi level.
- `boss.ogg`: phát khi boss chú ý player và bắt đầu combat.
- Nhạc dừng tại game-over và victory.