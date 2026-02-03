# How to Build This AI-Powered 3D Catalog App in 10 Steps

Here is a simple guide to recreating this application, broken down into 10 manageable steps.

### 1. **Project Setup**
   - Create a new project using **Vite** (a fast build tool).
   - Choose **React** as the framework and **TypeScript** for safety.
   - Run: `npm create vite@latest viz-app -- --template react-ts`.

### 2. **Install Key Libraries**
   - Install the tools needed for 3D, AI, and data handling.
   - **Three.js**: For the 3D galaxy visualization (`npm i three @types/three`).
   - **OpenAI**: To connect to GPT-4 (`npm i openai`).
   - **PapaParse**: To read CSV files easily (`npm i papaparse`).

### 3. **Style with Tailwind CSS & Shadcn**
   - Install **Tailwind CSS** for easy styling.
   - Initialize **Shadcn UI** to get pre-built, beautiful components like Buttons and Inputs.
   - Configure your `tailwind.config.js` to support dark mode and custom colors.

### 4. **Prepare Your Data**
   - Export your catalog data (Cloud, Platform, Tools, etc.) as a **CSV file** (`data.csv`).
   - Place this file in the `public/` folder so the app can access it.
   - Define a TypeScript interface (e.g., `type DataItem = { ... }`) to match your CSV columns.

### 5. **Create the 3D Scene**
   - In `App.tsx`, set up a basic **Three.js scene**:
     - **Scene**: The container for 3D objects.
     - **Camera**: The "eye" looking at the scene.
     - **Renderer**: Draws the scene to the HTML canvas.
   - Use `OrbitControls` to allow the user to rotate and zoom.

### 6. **Visualize Data as Particles**
   - Loop through your loaded data and create a **Particle System**.
   - Assign each particle a position in 3D space.
   - **Cluster Logic**: Group particles by "Cloud" (e.g., all AWS nodes in one area, Azure in another) using simple math coordinates.
   - **Color Coding**: Assign different colors to each cloud for visual distinction.

### 7. **Build the Sidebar & UI**
   - Create a sidebar on the left using standard HTML/React divs.
   - Add **Input fields** for filtering (Name, ID, Cloud).
   - Display the list of visible items in the sidebar.
   - Add a **"Details Panel"** that appears when a user clicks a node or list item.

### 8. **Implement AI Search**
   - Use the **OpenAI API** to interpret user questions.
   - Send the user's natural language query (e.g., *"Show me Azure databases"*) to GPT-4.
   - Ask GPT-4 to return **JSON** containing structured filters (e.g., `{ "Cloud": "Azure", "global": "database" }`).
   - Apply these filters to your data array.

### 9. **Add Interaction & Polish**
   - **Focus Logic**: When a user clicks an item, fly the camera to that specific particle using `controls.target`.
   - **Filtering**: When filters change, update the particle sizes (make non-matches tiny or invisible).
   - **Match Score**: Calculate a simple percentage match between the query words and the item's metadata to show relevancy.

### 10. **Final Features**
   - **Export**: Add a button to download the filtered list as a CSV.
   - **Copy Details**: Add a button to copy the item's full metadata to the clipboard.
   - **Deployment**: Run `npm run build` to create a production-ready folder (`dist/`) that can be hosted anywhere.

What is the project ?
- User give input to AI system that can automate browser action like click + type 
- Based on the user input as a “prompt” the ai system need to understand the user goal + end result + use-case + what need to be performed + browser actions
- Ai system need to use “playwright” as the web browser automation engine for the task 
- Ai system need to generate playwright tsx file that can perform action in browser 
- The Ai system can be OpenAi API KEY or Ollama API ends 
- User can use any of the above AI API provider
- If any error in the playwright action, if its not able to meet the user defined needful action that need to be preformed in the browser then fix the playwright tsx file then retry until the actual goal completed
- Make a score system that can help to work efficiently and fix errors by its own 
- The default browser will be chrome 
- This should be compatible with Mac, ubuntu, windows11 
- No unwanted markdown file need to generated or create at the file for build or error fix 
- Make a copy of playwright in the code repo
- For dev only use the MCP for playwright in the map tools session 
- No GUI for this version, but will be add one later 


Below mentioned file need to be create first in order to start building the profile.
- Docs
    - Build-Plan.md
        - Objective 
        - Goal
        - Tech Stack
        - Logical workflow 
        - Out come
    - Workflow.md
    - Phase1-build.md
    - Phase2-build.md
    - Phase3-build.md
Each each  mentioned md for that point I I’ll do a review on the build plan and setup that we will be in the next stage.  
