# Quick Start: Activate Visual Crossing Weather Backfill

When you're ready to run it, follow these 3 steps:

## Step 1: Get API Key (2 minutes)

1. Go to: https://www.visualcrossing.com/sign-up
2. Sign up (free, no credit card)
3. Copy your API key

## Step 2: Add to .env (30 seconds)

```bash
cd Backend
echo 'VISUALCROSSING_API_KEY="your_key_here"' >> .env
```

## Step 3: Test & Run (5-10 minutes)

### Test Setup:

```bash
python test_visualcrossing_setup.py
```

Should show Monza 2024 weather if working!

### Dry Run (preview):

```bash
python scripts/backfill_historical_weather.py --dry-run
```

### Run Full Backfill:

```bash
# Conservative (overnight, safest):
python scripts/backfill_historical_weather.py

# OR aggressive (6 minutes, fast):
python scripts/backfill_historical_weather.py --rate 1.0
```

---

## That's It!

The script will:

- ✓ Fetch weather for ~370 races
- ✓ Cache results (survives interruptions)
- ✓ Skip races with existing data
- ✓ Show progress live

**Full documentation:** See `VISUAL_CROSSING_SETUP.md`

---

## Files Ready:

✅ `api_clients/visualcrossing_client.py` - API client  
✅ `scripts/backfill_historical_weather.py` - Backfill script  
✅ `app/core/config.py` - Config updated  
✅ `.env.example` - Documented  
✅ `test_visualcrossing_setup.py` - Test script  
✅ `VISUAL_CROSSING_SETUP.md` - Full docs

Just add your API key when ready! 🚀
