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

## اجرا (Docker Compose v2)

> نکته: از «Docker Compose v2» استفاده کنید (دستور `docker compose` با فاصله)، نه نسخهٔ قدیمی `docker-compose`.

1) یک فایل env. بسازید (محلی و غیرقابل‌Commit)

```bash
cp env.sample .env
# سپس مقادیر را در .env اصلاح کنید (رمز دیتابیس و ...)
```

2) سرویس‌ها را بالا بیاورید

```bash
docker compose up -d --build
```

3) وضعیت و سلامت سرویس‌ها

```bash
docker compose ps
curl -sS http://localhost:8088/health
```

4) Traefik

- EntryPoint "web": `http://localhost:8088/`
- مسیر سلامت API (پروکسی Traefik): `http://localhost:8088/health`

## تنظیمات مهم Compose

- **`services.api.env_file: [.env]`**
  - متغیرهای محیطی را از فایل `.env` (لوکال و غیرقابل Commit) بارگذاری می‌کند. یک نمونه با مقادیر پیش‌فرض در `env.sample` قرار دارد.

- **`services.api.pull_policy: never`**
  - Compose را مجبور می‌کند ایمیج ریموت را Pull نکند و از ایمیج لوکالی که با بلوک `build` ساخته می‌شود استفاده کند. این کار از خطاهای قدیمی مانند `KeyError: 'ContainerConfig'` در ابزارهای legacy جلوگیری می‌کند.

- **`services.api.build` + `services.api.image`**
  - هر دو وجود دارند تا ایمیج به‌صورت لوکال Build شده و با تگ registry نیز برچسب بخورد؛ اما به‌دلیل `pull_policy: never` تلاش برای Pull ریموت انجام نمی‌شود.

## توقف و پاک‌سازی

```bash
docker compose -f docker-compose.yaml -f docker-compose.override.yaml down
```

## نکتهٔ سازگاری

- کلید قدیمی `version:` در فایل‌های Compose توسط نسخه‌های جدید نادیده گرفته می‌شود. در صورت تمایل می‌توان آن را حذف کرد تا هشدار نمایش داده نشود.

> این README در هر مرحله به‌روزرسانی می‌شود تا وضعیت فعلی پروژه را منعکس کند.
