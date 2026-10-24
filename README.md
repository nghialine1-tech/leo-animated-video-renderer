# 🎬 Leo Animated Story - Cloud Video Render (GitHub Actions)

Tự động hóa kết xuất video hoạt hình 3D Pixar chú gấu Leo học tiếng Anh chuẩn A1 (60 giây) hoàn toàn trên đám mây **GitHub Actions**, không tiêu tốn tài nguyên máy tính cá nhân.

---

## 🚀 Tính Năng Video
* **10 Phân Cảnh (60.0s)**: 3D Pixar Animation phong cách gấu Leo ấm áp, khăn đỏ và ba lô xanh.
* **Hook 3s Đầu Tiên**: Cú giật sự chú ý với câu hỏi tương tác & tiếng chuông tò mò *Ding!*.
* **Dynamic Karaoke Subtitles**: Phụ đề tiếng Anh A1 nhảy động từng từ, phóng to vàng neon kèm chấm vàng nảy nhịp nhàng theo giọng đọc + dịch nghĩa tiếng Việt.
* **Sunbeam Sparkles**: Bụi nắng vàng hoạt hình bay lơ lửng, tạo chiều sâu không gian điện ảnh.
* **Âm Thanh 3 Tầng**: Voiceover `en-US-AnaNeural` + Bộ hiệu ứng thực tế (SFX chân thực) + Nhạc nền Kalimba êm dịu.

---

## ⚡ Cách Chạy Render Trên GitHub Actions
1. Vào tab **Actions** trên GitHub Repository này.
2. Chọn workflow **"Render Leo Animated Video (60s Master)"**.
3. Bấm **"Run workflow"** -> Chọn nhánh `main` -> Bấm nút xanh **Run workflow**.
4. Chờ ~1 phút: Máy ảo Ubuntu của GitHub sẽ tự động dựng và xuất file MP4 tải về ở mục **Artifacts**!

---

## 📲 Cấu Hình Gửi Tự Động Về Telegram (Tùy Chọn)
Vào **Settings** -> **Secrets and variables** -> **Actions** -> Thêm Secret:
* `TELEGRAM_BOT_TOKEN`: Token của Bot Telegram của bạn.
* `TELEGRAM_CHAT_ID`: `5057026434` (hoặc ID Telegram của bạn).
