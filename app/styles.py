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
        padding:0;
    }


    .collapsible {
        border: none;
        background: $surface-darken-1;
        
    }

    .collapsible > CollapsibleTitle {
        background: $surface;
        color: $text;
        border: none;
        text-style: bold;
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

    .section-header {
        text-align: center;
        text-style: bold;
        background: $primary;
        color: $text;
        width: 100%;
        margin-top: 1;
        padding: 0 1;
    }

    .relationships-container {
        border: solid $secondary;
        padding: 0 1;
        background: $surface-darken-1;
        height: auto;
        margin-bottom: 1;
    }
    
    .relationship-item {
        color: $text-muted;
    }
    
    /* 
       Grid Area: SQL Editor 
       Column: 3, Row: 1 
    */
    #sql-area {
        column-span: 1;
        row-span: 1;
        padding:0;
        layers: base overlay;
    }

    #btn-run {
        background: $success;
        color: $text;
    }

    #sql-editor {
        height: 1fr;
        layer: base;
        border:none;
        background:$surface-darken-1
    }

    .floating-run-btn {
        dock: right;
        offset-y: 0;
        margin-right: 1;
        min-width: 10;
        height: 1;
        border: none;
        background: $success;
        color: $text;
        layer: overlay;
        opacity: 0.9;
    }

    /* 
       Grid Area: Schemas 
       Column: 2, Row: 2 
    */
    #schemas-area {
        column-span: 1;
        row-span: 1;
        overflow-y: auto;
        scrollbar-visibility: hidden;
    }

    .schema-inner {
        height: auto;
        background: $surface-darken-1;
    }

    .schema-inner DataTable {
        height: auto;
        background: $surface-darken-1;
    }

    /* 
       Grid Area: Console 
       Column: 3, Row: 2 
    */
    #console-area {
        column-span: 1;
        row-span: 1;
    }

    #console-log{
        background: $surface-darken-1;
        height:12%;
        border:none;
        scrollbar-visibility: hidden;
    }
    .dt_table{
        background: $surface-darken-1;
        border:none;
    }

    
    .sample_btn {
        background: $primary;
        color: $text;
        border: none;
    }

    .sample-btn-container {
        align: right middle;
        height: auto;
        width: 100%;
        padding-top: 1;
        padding-right: 1;
    }
    
    #btn-refresh {
        width: 100%;
        background: $warning;
        color: $text;
    }

    #questions{
        overflow-y:auto;
        height:95%
    }
   
   .schema-table{
        height: auto;
        background: $surface-darken-1;
        border:none;
        width:90%

   }
    """
