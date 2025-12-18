# Plan 06: Remove Tutorial Feature Entirely

## Objective
Completely remove the interactive tutorial system that was added, cleaning up all related files, database migrations, code, and UI elements.

## Rationale
The Driver.js tutorial library encountered CDN loading issues and added unnecessary complexity. Removing it will simplify the codebase and reduce external dependencies.

## Implementation Steps

### 1. Remove Tutorial-Related Database Changes
**Files to modify:**
- `accounts/models.py`
  - Remove `UserProfile` model
  - Remove signal handlers (`create_user_profile`, `save_user_profile`)

**Action:**
- Delete UserProfile model entirely
- Keep the User model unchanged

### 2. Remove Tutorial Views and URLs
**Files to modify:**
- `core/views.py`
  - Remove `tutorial_complete()` view
  - Remove `tutorial_dismiss()` view
  - Remove `tutorial_reset()` view
  - Remove imports: `JsonResponse`, `require_POST`

- `core/urls.py`
  - Remove all 3 tutorial URL patterns:
    - `path('tutorial/complete/', ...)`
    - `path('tutorial/dismiss/', ...)`
    - `path('tutorial/reset/', ...)`

### 3. Remove Tutorial Static Files
**Files to delete:**
- `core/static/core/js/tutorial.js`
- `core/static/core/css/tutorial-overrides.css`

### 4. Remove Tutorial from Templates
**Files to modify:**
- `accounts/templates/accounts/base.html`
  - Remove Driver.js CDN links (lines 14-17)
  - Remove tutorial CSS override link
  - Remove tutorial button from navigation bar (lines 231-239)
  - Remove tutorial script include (line 295)
  - Remove auto-launch script (lines 297-319)

- `core/templates/core/dashboard.html`
  - Remove tutorial buttons from welcome box (lines 79-93)
  - Revert welcome box to original text-only layout

### 5. Remove Tutorial References from Docs
**Files to update:**
- `CHANGELOG.md` - Add note about tutorial removal if applicable

### 6. Delete Tutorial Migration
**Action:**
- Keep the migration file in git history (don't delete it)
- Run `python manage.py migrate accounts zero` to revert the UserProfile table
- Or simply leave it - it won't cause issues if table isn't used

**Note:** We're NOT deleting the migration file itself, just not using it.

### 7. Verify No Broken References
After removal, check for any remaining references:
- Search codebase for "tutorial" (should find none)
- Search for "UserProfile" (should find none in business logic)
- Test that dashboard loads without errors
- Test that navigation works without errors

## Rollback Steps
If you want to restore the tutorial later:
1. Revert the git commit
2. Run migrations forward again
3. The static files and template code will be restored

## Success Criteria
✅ No tutorial-related code in models.py
✅ No tutorial-related code in views.py
✅ No tutorial-related code in urls.py
✅ No tutorial-related static files
✅ No tutorial buttons or scripts in templates
✅ Dashboard loads without errors
✅ All navigation works
✅ No console errors related to tutorial or Driver.js
✅ No database errors (UserProfile table unused but harmless)

## Time Estimate
~15 minutes for removal
~5 minutes for testing
