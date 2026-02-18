CSS = """
    Screen {
        layout: grid;
        grid-size: 3 2;
        grid-columns: 20% 40% 40%;
        grid-rows: 50% 50%;
        grid-gutter: 0;
        padding: 1;
        background: $surface;
    }

    /* Common Card Styling */
    .card {
        border: solid $primary;
        padding: 1;
        background: $surface-darken-1;
        height: 100%;
        width: 100%;
    }

    /* 
       Grid Area: Sidebar 
       Column: 1, Row: 1 & 2 (span 2)
    */
    #sidebar {
        column-span: 1;
        row-span: 2;
    }
    .collapsible {
        border: none;
        background: $surface-darken-1;
    }

    .collapsible > CollapsibleTitle {
        background: $surface-darken-1;
        color: $text;
        border: none;
    }

    .collapsible > CollapsibleTitle:focus {
        background: $surface-darken-1;
        color: $text;
        border: none;
    }

    .collapsible > CollapsibleTitle:hover {
        background: $surface-darken-1;
        color: $text;
    }

    .collapsible > CollapsibleBody {
        background: $surface-darken-1;
        border: none;
    }

    .collapsible > CollapsibleBody:focus-within {
        background: $surface-darken-1;
        border: none;
    }

    .collapsible > CollapsibleBody:hover {
        background: $surface-darken-1;
        color: $text;
    }
    
    #sidebar ListView {
        height: auto;
        margin-bottom: 1; 
        background: $surface-darken-1;
    }

    /* 
       Grid Area: Topic 
       Column: 2, Row: 1 
    */
    #topic-area {
        column-span: 1;
        row-span: 1;
    }

    .topic-header {
        height: auto;
        border: heavy $secondary;
        padding: 1;
        margin-bottom: 1;
        text-align: center;
        text-style: bold;
    }
    
    #btn-hints {
        width: 100%;
        margin-top: 1;
        background: $warning;
        color: $surface;
    }

    /* 
       Grid Area: SQL Editor 
       Column: 3, Row: 1 
    */
    #sql-area {
        column-span: 1;
        row-span: 1;
    }

    .sql-toolbar {
        height: auto;
        align: right middle;
        margin-bottom: 1;
    }

    #btn-run {
        background: $success;
        color: $text;
    }

    #sql-editor {
        height: 1fr;

    }

    /* 
       Grid Area: Schemas 
       Column: 2, Row: 2 
    */
    #schemas-area {
        column-span: 1;
        row-span: 1;
        overflow-y: auto;
    }

    /* 
       Grid Area: Console 
       Column: 3, Row: 2 
    */
    #console-area {
        column-span: 1;
        row-span: 1;
    }

    #console-log {
        height: 1fr;
        background: $surface-darken-1;
        border: blank;
    }

    #sample-data-table {
        height: 1fr;
        border: blank;
        background: $surface-darken-1;
    }
    
    .sample-btn {
        margin-top: 1;
        width: 100%;
    }
    """
