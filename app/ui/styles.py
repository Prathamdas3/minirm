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
        padding:0;
        layers: base overlay;
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
        width: auto;
        min-width: 16;
        height: 1;
    }

    /* DB Management */
    #db-list {
        height: auto;
        max-height: 50%;
        margin-bottom: 1;
        background: $surface-darken-1;
    }
    
    .db-item-row {
        height: auto;
        width: 100%;
        align-vertical: middle;
        layout: horizontal;
    }

    .db-path-label {
        width: 1fr;
    }

    .remove-db-btn {
        width: 4;
        min-width: 4;
        height: 1;
        background: $error;
        color: $text;
        margin-left: 1;
        padding: 0;
        border: none;
    }

    
    /* Input Screen */
    DBInputScreen {
        align: center middle;
        background: $surface 50%;
    }

    #dialog {
        grid-size: 2;
        grid-gutter: 1 2;
        grid-rows: 1fr 3;
        padding: 1 2;
        width: 60;
        height: 14;
        border: thick $background 80%;
        background: $surface;
    }

    #dialog-title {
        column-span: 2;
        height: 1;
        width: 100%;
        content-align: center middle;
        text-style: bold;
    }

    #path-input {
        column-span: 2;
        width: 100%;
    }

    #btn-submit-db {
        column-span: 2;
        width: 100%;
        margin-top: 1;
        background: $primary;
        color: $text;
    }
    
    #btn-cancel-db {
        column-span: 2;
        width: 100%;
        margin-top: 1;
        background: $error; 
        color: $text;
    }
    
    .sample-btn-container {
        align: right middle;
        height: auto;
        width: 100%;
        padding-top: 1;
    }
    
    #sidebar_buttons_container{
        layout:horizontal;
        height:10%;
    }
    
    .sidebar_btn{
        border:solid $primary;
        background: $surface-darken-1;
        width:50%;
        margin:1
    }
    
    #db_list{
        overflow-y:auto;
        height:20%;
    }
    #questions{
        overflow-y:auto;
        height:72%
    }
    """
