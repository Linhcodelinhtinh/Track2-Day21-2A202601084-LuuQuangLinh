# Báo Cáo Lab Day 21 - CI/CD cho AI Systems

| | |
|---|---|
| Họ và tên | Lưu Quang Linh |
| MSSV | 2A202601084 |
| Lớp / Khóa | K4 |
| Repo GitHub | https://github.com/Linhcodelinhtinh/Track2-Day21-2A202601084-LuuQuangLinh |
| Ngày nộp | 21/08/2026 |

---

## 1. Bộ Siêu Tham Số Đã Chọn và Lý Do

| Lần chạy | n_estimators | learning_rate | max_depth | f1_score | accuracy |
|---|---|---|---|---|---|
| 1 | 100 | 0.1 | 3 | 0.7109 | 0.8710 |
| 2 | 200 | 0.05 | 5 | 0.7037 | 0.8720 |
| 3 | 80 | 0.2 | 2 | 0.6986 | 0.8740 |

**Bộ siêu tham số đã chọn:** `n_estimators=100`, `learning_rate=0.1`, `max_depth=3`.

**Lý do:** Bộ siêu tham số này đạt chỉ số f1_score cao nhất (0.7109) trên tập đánh giá holdout. Đáng chú ý, lần chạy 3 đạt accuracy cao nhất (0.8740) nhưng f1_score chỉ đạt 0.6986, cho thấy accuracy bị ảnh hưởng bởi lớp đa số (thu nhập <=50K) trong khi f1_score phản ánh chính xác khả năng phân loại lớp dương. Ngoài ra, việc gia tăng n_estimators và giảm learning_rate (lần 2) làm tăng độ phức tạp của mô hình và nguy cơ quá khớp, dẫn đến f1_score giảm nhẹ.

---

## 2. Vì Sao Ngưỡng Chất Lượng Đặt Trên F1 Chứ Không Phải Accuracy

Bộ dữ liệu Adult mang tính mất cân bằng lớp rõ rệt khi lớp thu nhập <=50K (lớp âm) chiếm khoảng 75% và lớp thu nhập >50K (lớp dương) chỉ chiếm 25%. Một mô hình ngây thơ luôn dự đoán mọi mẫu là "thu nhập thấp" vẫn đạt được accuracy 0.75 (75%) mà không học được bất kỳ quy luật nào, khiến chỉ số accuracy gây hiểu nhầm nghiêm trọng. f1_score của lớp dương là trung bình điều hòa giữa Precision và Recall, đo lường chính xác khả năng phát hiện đúng người có thu nhập cao. Ta không dùng average="weighted" hay average="macro" vì các tùy chọn này tính trung bình cả lớp âm đa số, làm mờ đi hiệu năng trên lớp dương cần theo dõi.

---

## 3. Khó Khăn Gặp Phải và Cách Giải Quyết

| Khó khăn | Nguyên nhân | Cách giải quyết |
|---|---|---|
| SSH key bị từ chối quyền truy cập khi deploy EC2 | Phân quyền file `demoday21.pem` mặc định `0444` quá mở trên Windows/WSL | Copy file key vào `~/.ssh/demoday21.pem`, phân lại quyền `chmod 400` và trỏ đúng tham số `-i` |
| Service `income-api` crash liên tục khi unpickle model | Xung đột phiên bản scikit-learn giữa CI/CD và EC2 do Ubuntu 26.04 chạy Python 3.14 không tương thích | Tạo môi trường ảo độc lập bằng Python 3.10/3.11 và cài đặt đồng bộ phiên bản `scikit-learn==1.4.2` cùng các phụ thuộc |
| Lỗi đường dẫn Windows trong pytest MLflow (`PermissionError`) | MLflow mặc định ghi vào Experiment 0 chứa đường dẫn tuyệt đối dạng `file:///C:/...` | Tạo Experiment tên riêng biệt (`Income_Model`) với `artifact_location` dạng URI chuẩn và cô lập MLFLOW_TRACKING_URI |

---

## 4. So Sánh Bước 2 và Bước 3

| | f1_score | accuracy |
|---|---|---|
| Bước 2 (chỉ `train_batch1`) | 0.7109 | 0.8710 |
| Bước 3 (thêm `train_batch2`) | 0.7091 | 0.8715 |

**Nhận xét:** Khi bổ sung tập dữ liệu `train_batch2` mở rộng dung lượng từ 22.361 lên 44.722 mẫu (và thậm chí 67.803 mẫu), chỉ số f1_score về cơ bản giữ mức ổn định (giảm nhẹ 0.0018) trong khi accuracy tăng nhẹ. Điều này thể hiện tập dữ liệu mới có cùng phân phối với tập dữ liệu ban đầu và không cung cấp thêm các mẫu biên đột phá cho lớp dương (>50K), cho thấy việc bổ sung dữ liệu không phải lúc nào cũng làm tăng chỉ số F1.
