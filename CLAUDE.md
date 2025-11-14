# CLAUDE.md - AI Assistant Guide for Certificate Center

## Project Overview

**Certificate Center** is a Streamlit-based web application that automates certificate generation. Users can upload a blank certificate template and add customized text (typically names) with configurable fonts, sizes, and positioning.

**Tech Stack:**
- Python 3.x
- Streamlit (web framework)
- OpenCV (opencv-python-headless) for image processing
- Pillow (PIL) for image handling
- NumPy for array operations

**Deployment:** Configured for Heroku deployment with Procfile and setup.sh

## Repository Structure

```
certificate-center/
├── app.py                  # Main application file (Streamlit app)
├── requirements.txt        # Python dependencies
├── Procfile               # Heroku deployment configuration
├── setup.sh               # Streamlit configuration for Heroku
├── README.md              # User-facing documentation
├── Certificate.png        # Sample certificate template
├── certification.png      # App logo/icon
└── .git/                  # Git repository
```

## Key Files and Their Purpose

### app.py (3785 bytes, 119 lines)
**Purpose:** Main application entry point

**Key Components:**
- **Lines 1-5:** Import dependencies (streamlit, cv2, PIL, numpy, os)
- **Lines 8-12:** App configuration and logo setup
- **Lines 14-47:** User input collection (name, font, size, coordinates, file upload)
- **Lines 52-118:** Certificate generation logic on submit
  - Font selection mapping (lines 56-73)
  - Image processing with NumPy (lines 79-81)
  - Text positioning calculation (lines 84-92)
  - Text rendering with OpenCV (lines 93-97)
  - File save and download (lines 99-118)

**Important Variables:**
- `font_color = (0,0,0)` - Black text color (BGR format)
- `certi_path = 'certi.png'` - Temporary output file name
- Font options map to OpenCV font constants (FONT_HERSHEY_*)

### requirements.txt
**Dependencies:**
- `streamlit` - Web framework
- `opencv-python-headless` - OpenCV without GUI dependencies (Heroku-compatible)
- `Pillow` - Image processing library
- `numpy` - Numerical operations

**Note:** Uses opencv-python-headless instead of opencv-python for deployment compatibility

### Procfile
Heroku dyno configuration: `web: sh setup.sh && streamlit run app.py`
- Runs setup script first to configure Streamlit
- Then starts the Streamlit app

### setup.sh
Creates Streamlit config for headless Heroku deployment:
- Sets headless mode
- Configures port from environment variable
- Disables CORS

## Code Conventions

### Python Style
- **No explicit style guide enforced** - code uses standard Python conventions
- Indentation: 4 spaces
- Variable naming: snake_case (e.g., `font_color`, `certi_name`)
- No type hints currently used
- Inline comments for clarity

### Image Processing Patterns
1. **Image Loading:** File upload → bytes → numpy array → cv2.imdecode
2. **Coordinate System:** OpenCV uses (x, y) where origin is top-left
3. **Color Format:** BGR (not RGB) - `(0,0,0)` is black
4. **Text Positioning:** Center-based calculation with user adjustments
5. **File Cleanup:** Temporary files removed after download (line 118)

### Streamlit Patterns
- User inputs defined before submit button
- Processing logic inside `if submit:` block
- Error handling for missing inputs (line 53-54)
- Preview display before download option

## Development Workflow

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
streamlit run app.py
```

### Making Changes

**Common Modification Points:**
1. **Font Options:** Modify lines 18-29 to add/remove fonts
2. **Font Size Range:** Modify line 33 to adjust size options
3. **Default Colors:** Modify line 9 for different text colors
4. **Input Validation:** Add checks in the submit block (around line 53)
5. **Image Format Support:** Modify line 47 to add formats (currently png, jpg)

**Testing Checklist:**
- [ ] Test with various certificate templates
- [ ] Verify text positioning with different coordinates
- [ ] Test all font options
- [ ] Verify download functionality
- [ ] Check file cleanup (no leftover certi.png files)

### Deployment to Heroku
```bash
git add .
git commit -m "Description of changes"
git push heroku main
```

**Environment Requirements:**
- Heroku buildpack: Python
- PORT environment variable (auto-set by Heroku)

## Git Workflow

### Branch Structure
- **main/master:** Production branch
- **Feature branches:** Use pattern `claude/claude-md-{identifier}` for AI assistant work

### Commit Message Patterns (from history)
- "Update app.py" - Simple file updates
- "Updated requirements.txt" - Dependency changes
- "User can upload their own certificate" - Feature additions
- "changed opencv to opencv headless version" - Technical improvements

### Recent Development History
Key commits show evolution:
1. Changed to opencv-headless for deployment compatibility
2. Added user certificate upload feature
3. Regular updates to requirements and app logic

## Important Notes for AI Assistants

### When Modifying app.py

**DO:**
- ✅ Test font constant mappings if changing font options
- ✅ Maintain the temporary file cleanup pattern (os.remove)
- ✅ Preserve the center-based text positioning logic
- ✅ Keep error handling for missing name/file inputs
- ✅ Use opencv-python-headless in requirements.txt
- ✅ Ensure coordinate inputs accept negative values for flexibility

**DON'T:**
- ❌ Change opencv-python-headless to opencv-python (breaks Heroku)
- ❌ Remove the setup.sh file (needed for Heroku)
- ❌ Hardcode file paths (use relative paths)
- ❌ Leave temporary files without cleanup
- ❌ Use RGB color format (OpenCV uses BGR)

### Security Considerations
- File uploads limited to .png and .jpg (line 47)
- Temporary files cleaned up to prevent disk filling
- No user data persistence (stateless application)
- Consider adding file size limits for uploads
- Sanitize user input for filenames in download

### Performance Notes
- Certificate generation is synchronous (blocks UI)
- For high-traffic scenarios, consider:
  - Adding progress indicators
  - Implementing async processing
  - File size validation
  - Memory cleanup for large images

### Common Debugging Points

**Issue:** Text not appearing on certificate
- Check: font_color vs background color contrast
- Check: Coordinates within image bounds
- Check: Font multiplier not set to 0

**Issue:** Image upload fails
- Check: File format in allowed list (line 47)
- Check: File size (no explicit limit currently)
- Check: Image decode step (line 81)

**Issue:** Download not working
- Check: certi.png exists before download
- Check: File permissions
- Check: Browser download settings

## API Reference

### OpenCV Font Constants Used
- `cv2.FONT_HERSHEY_SIMPLEX` - Normal sans-serif
- `cv2.FONT_HERSHEY_PLAIN` - Small sans-serif
- `cv2.FONT_HERSHEY_DUPLEX` - Complex sans-serif
- `cv2.FONT_HERSHEY_COMPLEX` - Normal serif
- `cv2.FONT_HERSHEY_TRIPLEX` - Complex serif
- `cv2.FONT_HERSHEY_COMPLEX_SMALL` - Small serif
- `cv2.FONT_HERSHEY_SCRIPT_SIMPLEX` - Hand-writing
- `cv2.FONT_HERSHEY_SCRIPT_COMPLEX` - Complex hand-writing

### Key OpenCV Functions
- `cv2.imdecode(buf, flags)` - Decode image from buffer
- `cv2.getTextSize(text, font, scale, thickness)` - Calculate text dimensions
- `cv2.putText(img, text, org, font, scale, color, thickness)` - Draw text
- `cv2.imwrite(filename, img)` - Save image to file

## Future Enhancement Opportunities

1. **Multi-language Support:** Add Unicode font support for non-English names
2. **Batch Processing:** Upload CSV to generate multiple certificates
3. **Template Library:** Pre-loaded certificate templates
4. **Color Picker:** UI for custom text colors
5. **Preview Mode:** Real-time preview before final generation
6. **Advanced Positioning:** Visual coordinate picker
7. **Font Upload:** Allow custom .ttf font files
8. **Output Formats:** Support PDF output
9. **Database Integration:** Save generated certificates
10. **Authentication:** User accounts for certificate history

## Quick Command Reference

```bash
# Local development
streamlit run app.py

# Install dependencies
pip install -r requirements.txt

# Check Python version
python --version

# View Streamlit config
streamlit config show

# Clear Streamlit cache
streamlit cache clear

# Git operations
git status
git add .
git commit -m "message"
git push origin branch-name
```

## Contact & Resources

- **Live App:** https://bit.ly/3Cxfkhy
- **Streamlit Docs:** https://docs.streamlit.io
- **OpenCV Python Docs:** https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html

---

**Last Updated:** 2025-11-14
**Repository:** certificate-center
**For AI Assistants:** This guide is optimized for Claude and other AI coding assistants to quickly understand and work with this codebase.
