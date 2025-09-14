# DevOps Local Starter (Step-by-Step)

هدف: ساخت یک پروژه‌ی **DevOps لوکال** از صفر تا صد، به‌صورت **مرحله‌ای، قابل اجرا، و قابل توضیح**.

## فلسفه
- هر مرحله یک خروجی قابل اجرا دارد.
- هر فایل با توضیح مفهوم، دلیل طراحی، و شیوه‌ی اجرا ارائه می‌شود.
- کیفیت کد (lint/test) و امنیت از روز اول بخشی از چرخه‌اند.

## نقشه‌ی راه (خلاصه)
1) بوت‌استرپ: Docker Compose + Traefik + FastAPI + تست/لینت + pre-commit  
2) دیتابیس: PostgreSQL + Alembic + تست یکپارچه  
3) بک‌گراند جاب‌ها: Redis + Worker (Celery/RQ)  
4) لاگینگ ساخت‌یافته: Loki/Promtail + Grafana  
5) متریک و تریسینگ: Prometheus + OpenTelemetry (+ Tempo/Jaeger)  
6) امنیت: Trivy، gitleaks، سیاست‌های کامیت و نسخه‌بندی  
7) CI لوکال/دور: GitHub Actions (+ act لوکال)  
8) پکیجینگ و ریلیز: نسخه‌بندی، ایمیج‌ها  
9) Kubernetes لوکال: kind/k3d + Helm + GitOps (Argo CD)  
10) مدیریت Secrets: SOPS/age

## قوانین پروژه
- زبان کد سرویس نمونه: Python (FastAPI)
- کنترل کیفیت: pytest، black، isort، flake8، bandit
- کانتینرسازی: Dockerfile چندمرحله‌ای + Compose
- روتینگ: Traefik (v3)
- همه‌چیز لوکال و بدون نیاز به سرور

> این README در هر مرحله به‌روزرسانی می‌شود تا وضعیت فعلی پروژه را منعکس کند.
