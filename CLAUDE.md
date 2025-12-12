# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Kitchen management and purchase order system for a food business. Two main features:

1. **Raw Materials + Production Tracker** - Daily recording of raw materials consumed (meat, vegetables, oil, packaging with various measurements) and production output (food packs, platters/bilao, contents)

2. **Purchase Order Tracker** - Create, update, monitor purchase orders associated with customers. Orders can be fulfilled in full or staggered with update history (comment-style)

## Tech Stack

- **Backend**: Django
- **Frontend**: Tailwind CSS
- **Database**: PostgreSQL (Supabase)
- **Authentication**: Supabase Auth (not Django's built-in auth)
- **Hosting**: Vercel

## User Roles

- Admin (developer)
- Management (owner and secretary)

## Design Philosophy

Keep the system sleek and simple. Follow the owner's vision exactly - no feature creep or unsolicited additions.
