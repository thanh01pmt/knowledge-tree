#!/usr/bin/env python3
import json, csv, subprocess
from pathlib import Path

ROOT = Path("/Users/tonypham/MEGA/WebApp/content-gen/knowledge-tree")

def build_proj(proj: str, items: list):
    pdir = ROOT / "projects" / proj
    out_dir = pdir / "output"
    work_dir = pdir / ".work"
    out_dir.mkdir(parents=True, exist_ok=True)
    work_dir.mkdir(parents=True, exist_ok=True)

    slug = proj.replace("roadmap_sh_", "")
    json_path = pdir / "context" / f"{slug}.json"
    topics_list, subtopics_list = [], []
    if json_path.exists():
        with open(json_path, encoding="utf-8") as f:
            d = json.load(f)
        nodes = d.get("nodes", [])
        topics_list = [n.get("data", {}).get("label") for n in nodes if n.get("type") == "topic" and n.get("data", {}).get("label")]
        subtopics_list = [n.get("data", {}).get("label") for n in nodes if n.get("type") == "subtopic" and n.get("data", {}).get("label")]

    with open(work_dir / "context-audit.md", "w", encoding="utf-8") as f:
        f.write(f"# Context Syllabus Audit for {proj}\n\n## Core Topics\n")
        for t in topics_list:
            f.write(f"- {t}\n")
        f.write("\n## Subtopics & Detailed Skills\n")
        for st in subtopics_list:
            f.write(f"- {st}\n")

    fields = [["COMPUTING_AND_IT", "Computing & Information Technology", "Lĩnh vực công nghệ thông tin và khoa học máy tính."]]
    subjects = [["SOFTWARE_ENGINEERING_SE", "Software Engineering", "Môn học kỹ thuật phần mềm và hệ thống ứng dụng.", "COMPUTING_AND_IT"]]
    categories = [["SOFTWARE_SYSTEMS_ENGINEERING", "Software Systems Engineering", "Phân loại chuyên môn phát triển hệ thống phần mềm.", "SOFTWARE_ENGINEERING_SE"]]

    topic_rows, concept_rows, lo_rows = [], [], []

    for item in items:
        t_code, t_name, c_code, c_name, c_desc, keywords, ulo_code, ulo_name, ulo_desc, cio_code, cio_name, cio_desc, sios = item

        topic_rows.append([t_code, t_name, f"Chủ đề trọng tâm: {t_name}", "SOFTWARE_SYSTEMS_ENGINEERING"])
        concept_rows.append([c_code, c_name, c_desc, t_code, keywords, "", '{"icon": "code"}'])

        lo_rows.append([ulo_code, ulo_name, f"Người học có khả năng {ulo_desc}", "UNIVERSAL", "", c_code])
        lo_rows.append([cio_code, cio_name, f"Người học có khả năng {cio_desc}", "CONCEPTUAL_IMPL", ulo_code, c_code])

        for sio_code, sio_name, sio_desc in sios:
            lo_rows.append([sio_code, sio_name, f"Người học có khả năng {sio_desc}", "SPECIFIC_IMPL", cio_code, c_code])

    def write_tsv(fname, headers, data):
        with open(out_dir / fname, "w", encoding="utf-8", newline="") as f:
            w = csv.writer(f, delimiter="\t")
            w.writerow(headers)
            w.writerows(data)

    write_tsv("fields.tsv", ["code", "name", "description"], fields)
    write_tsv("subjects.tsv", ["code", "name", "description", "field_codes"], subjects)
    write_tsv("categories.tsv", ["code", "name", "description", "subject_codes"], categories)
    write_tsv("topics.tsv", ["code", "name", "description", "category_codes"], topic_rows)
    write_tsv("concepts.tsv", ["code", "name", "description", "topic_codes", "keywords", "cs2023_ka_mapping", "metadata"], concept_rows)
    write_tsv("learning-objectives.tsv", ["code", "name", "description", "lo_type", "parent_lo_code", "concept_codes"], lo_rows)

    val_res = subprocess.run(["python3", ".agents/skills/tree-validator/scripts/validate_tree.py", "--project", proj], capture_output=True, text=True)
    aud_res = subprocess.run(["python3", ".agents/skills/tree-validator/scripts/audit_coverage.py", "--project", proj], capture_output=True, text=True)
    
    val_last = val_res.stdout.strip().splitlines()[-1] if val_res.stdout else "N/A"
    aud_lines = [l for l in aud_res.stdout.splitlines() if "Coverage Score" in l or "Status" in l]
    
    print(f"✅ {proj:<24} | Concepts: {len(concept_rows):<2} | LOs: {len(lo_rows):<3} | Val: {val_last.split('—')[0].strip()} | Audit: {' | '.join(aud_lines)}")

# REACT (18 Concepts, 90 LOs)
react_items = [
    ("COMPONENT_BASED_ARCHITECTURE", "Component-Based UI Architecture", "DECLARATIVE_COMPONENT_TREE", "Declarative Component Trees & Virtual DOM", "Kiến trúc giao diện phân rã thành các linh kiện độc lập và cây Virtual DOM.", "JSX, Virtual DOM, React components, props, rendering, tree reconciliation", "ULO-COMPONENT-ARCHITECTURE", "Master Declarative Component Trees and Virtual DOM", "giải thích mô hình linh kiện và cơ chế đồng bộ Virtual DOM.", "CIO-COMPONENT-HIERARCHY-DESIGN", "Structure Declarative Component Trees and Props Flow", "phân rã giao diện thành cây component và luồng truyền props.", [
        ("SIO-REACT-FUNCTIONAL-COMPONENTS", "Build Functional Components with JSX", "khai báo các Functional Components bằng cú pháp JSX trong React."),
        ("SIO-REACT-PROPS-DESTRUCTURING", "Pass Props and Destructure Property Attributes", "truyền và trích xuất dữ liệu props giữa component cha và con."),
        ("SIO-REACT-VIRTUAL-DOM-RECONCILIATION", "Analyze Virtual DOM Diffing and Reconciliation", "giải thích thuật toán Diffing và quá trình Reconciliation trên cây Virtual DOM.")
    ]),
    ("STATE_MANAGEMENT_HOOKS", "State Management & React Hooks", "LOCAL_STATE_REACTIVE_HOOKS", "Local Component State & Reactive Hooks", "Quản lý trạng thái nội bộ component và vòng đời bằng Hooks.", "useState, useEffect, useReducer, custom hooks, reactive state, component lifecycle", "ULO-STATE-MANAGEMENT-HOOKS", "Master Component State Management and Reactive Hooks", "làm chủ quản lý trạng thái nội bộ và các Hooks.", "CIO-STATE-MUTATION-LIFECYCLE", "Mutate Component State and Handle Lifecycles", "cập nhật trạng thái và lắng nghe vòng đời qua useEffect.", [
        ("SIO-REACT-USESTATE-HOOK", "Manage Reactive State with useState Hook", "quản lý trạng thái nội bộ component bằng useState Hook."),
        ("SIO-REACT-USEEFFECT-LIFECYCLE", "Handle Side Effects and Cleanup with useEffect", "thực hiện tác vụ side-effect và dọn dẹp bộ nhớ bằng useEffect."),
        ("SIO-REACT-USEREDUCER-COMPLEX-STATE", "Manage Complex State Transitions via useReducer", "điều khiển các chuyển đổi trạng thái phức tạp bằng useReducer.")
    ]),
    ("CUSTOM_HOOKS_COMPOSITION", "Custom Hooks & Logic Reusability", "REUSABLE_CUSTOM_HOOKS", "Custom Hook Composition & Logic Extraction", "Tách rã và tái sử dụng logic giao diện thông qua Custom Hooks.", "custom hooks, logic extraction, composition, reuse, custom stateful logic", "ULO-CUSTOM-HOOKS", "Master Custom Hook Composition and Logic Extraction", "tách rã logic tái sử dụng thành Custom Hooks.", "CIO-STATEFUL-LOGIC-COMPOSITION", "Compose Stateful Logic Functions across Components", "chia sẻ logic trạng thái giữa các linh kiện.", [
        ("SIO-REACT-BUILD-CUSTOM-HOOK", "Extract Custom Hook Logic Functions", "xây dựng Custom Hook riêng bắt đầu bằng tiền tố use."),
        ("SIO-REACT-HOOKS-RULES-ENFORCE", "Enforce Rules of Hooks Guidelines", "tuân thủ các quy tắc gọi Hooks (Rules of Hooks)."),
        ("SIO-REACT-COMPOSE-MULTIPLE-HOOKS", "Combine Multiple Primitive Hooks", "kết hợp nhiều primitive Hooks bên trong một Custom Hook.")
    ]),
    ("CONTEXT_GLOBAL_STATE", "Context API & Global State Sharing", "CONTEXT_PROP_DRILLING_PREVENTION", "Context API & Global State Sharing", "Chia sẻ dữ liệu toàn cục tránh hiện tượng Prop Drilling qua Context API.", "createContext, useContext, Provider, prop drilling, global state", "ULO-CONTEXT-GLOBAL-STATE", "Master Context API and Global State Sharing", "chia sẻ trạng thái toàn cục qua Context API.", "CIO-PROVIDER-CONSUMER-PATTERN", "Implement Context Provider and Consumer Patterns", "tạo Provider bọc cây component để chia sẻ dữ liệu.", [
        ("SIO-REACT-CREATE-USE-CONTEXT", "Define Context Stores with createContext and useContext", "khởi tạo Context Store và sử dụng useContext Hook."),
        ("SIO-REACT-CONTEXT-PROVIDER-WRAP", "Wrap App Tree with Context Providers", "bọc các component con trong Provider để truyền giá trị toàn cục."),
        ("SIO-REACT-AVOID-PROP-DRILLING", "Eliminate Prop Drilling across Deep Trees", "khắc phục hiện tượng truyền props trùng lặp qua nhiều cấp (Prop Drilling).")
    ]),
    ("ROUTING_NAVIGATION_SYSTEM", "Single-Page Routing & Navigation Engine", "SINGLE_PAGE_ROUTING_ENGINE", "Single-Page Routing & Dynamic Navigation", "Điều hướng trang Single-Page Application (SPA), tham số URL và route động.", "React Router, Dynamic Routing, useNavigate, useParams, Link, SPA", "ULO-SINGLE-PAGE-ROUTING", "Master Single-Page Routing and Navigation Engines", "làm chủ phân tuyến đường dẫn trong ứng dụng SPA.", "CIO-DYNAMIC-ROUTE-MATCHING", "Match Dynamic Routes and URL Parameters", "phân tuyến và trích xuất tham số trên URL.", [
        ("SIO-REACT-ROUTER-DOM-SETUP", "Configure React Router DOM Route Trees", "khai báo danh sách đường dẫn bằng BrowserRouter và Routes."),
        ("SIO-REACT-USEPARAMS-NAVIGATE", "Extract URL Params with useParams and useNavigate", "trích xuất tham số đường dẫn bằng useParams và chuyển trang bằng useNavigate."),
        ("SIO-REACT-PROTECTED-ROUTES", "Guard Private Endpoints with Protected Routes", "bảo vệ đường dẫn yêu cầu đăng nhập bằng Protected Routes.")
    ]),
    ("FORM_HANDLING_VALIDATION", "Form Control & Input Validation", "FORM_CONTROL_VALIDATION", "Controlled Components & Input Schema Validation", "Quản lý form điều khiển (controlled components) và xác thực dữ liệu.", "React Hook Form, Formik, Zod, Yup, controlled components, validation", "ULO-FORM-CONTROL-VALIDATION", "Master Form Control and Input Schema Validation", "quản lý dữ liệu biểu mẫu và xác thực đầu vào.", "CIO-INPUT-SCHEMA-VERIFICATION", "Verify Form Data against Validation Schemas", "xác thực dữ liệu form theo quy tắc schema.", [
        ("SIO-REACT-CONTROLLED-INPUTS", "Manage Controlled Form Inputs with State", "quản lý giá trị ô nhập bằng Controlled Components."),
        ("SIO-REACT-HOOK-FORM-INTEGRATION", "Build High-Performance Forms with React Hook Form", "xây dựng biểu mẫu tối ưu tốc độ bằng React Hook Form."),
        ("SIO-REACT-ZOD-SCHEMA-VALIDATION", "Validate Form Schema Inputs via Zod", "xác thực dữ liệu đầu vào bằng thư viện Zod schema.")
    ]),
    ("PERFORMANCE_MEMOIZATION_OPT", "Performance Optimization & Memoization", "MEMOIZATION_PERFORMANCE_TUNING", "Memoization Utilities & Rendering Optimization", "Tối ưu hóa hiệu năng render bằng memo, useMemo, useCallback và virtualization.", "React.memo, useMemo, useCallback, Code Splitting, Lazy, Suspense, Virtualization", "ULO-PERFORMANCE-MEMOIZATION", "Master Memoization Utilities and Rendering Optimization", "tối ưu số lần re-render và hiệu năng hiển thị.", "CIO-RE-RENDER-ELIMINATION", "Eliminate Redundant Component Re-renders", "ngăn chặn re-render thừa bằng memoization.", [
        ("SIO-REACT-MEMO-HIGHER-ORDER", "Prevent Re-renders with React.memo", "bọc component bằng React.memo để chặn re-render khi props không đổi."),
        ("SIO-REACT-USEMEMO-USECALLBACK", "Cache Calculations with useMemo and useCallback", "ghi nhớ giá trị tính toán bằng useMemo và hàm bằng useCallback."),
        ("SIO-REACT-LAZY-SUSPENSE-SPLIT", "Code Split Bundles with React.lazy and Suspense", "tách nhỏ gói bundle bằng React.lazy() và Suspense.")
    ]),
    ("EXTERNAL_STATE_STORE_REDUX", "Global External State Management", "GLOBAL_EXTERNAL_STATE_MANAGEMENT", "External State Stores & Flux Architecture", "Quản lý trạng thái toàn cục phức tạp bằng Redux Toolkit hoặc Zustand.", "Redux Toolkit, Zustand, Flux, slice, actions, reducers, dispatch, useSelector", "ULO-EXTERNAL-STATE-MANAGEMENT", "Master External State Stores and Flux Architecture", "quản lý trạng thái ứng dụng lớn bằng các thư viện Redux/Zustand.", "CIO-ACTION-REDUCER-DISPATCH", "Dispatch Actions and Process Reducer Transformations", "gửi action và biến đổi state qua Reducers.", [
        ("SIO-REACT-REDUX-TOOLKIT-SLICE", "Define Redux Toolkit Slices and Reducers", "khai báo Redux Slice và các hàm xử lý reducer."),
        ("SIO-REACT-USEDISPATCH-USESELECTOR", "Dispatch Actions and Select State with Redux Hooks", "gửi action bằng useDispatch và đọc dữ liệu qua useSelector."),
        ("SIO-REACT-ZUSTAND-LIGHTWEIGHT-STORE", "Create Lightweight Global Stores with Zustand", "quản lý state toàn cục siêu nhẹ bằng Zustand store.")
    ]),
    ("ASYNC_DATA_FETCHING_TANSTACK", "Async Data Fetching & Server State", "SERVER_STATE_DATA_FETCHING", "Server State Caching & Async Data Fetching", "Quản lý trạng thái phía server, cache dữ liệu và tự động làm mới qua TanStack Query.", "TanStack Query, React Query, useQuery, useMutation, caching, stale-while-revalidate", "ULO-SERVER-STATE-DATA-FETCHING", "Master Server State Caching and Async Data Fetching", "quản lý trạng thái server và cache dữ liệu API.", "CIO-CACHE-INVALIDATION-REFETCH", "Invalidate Cache Keys and Refetch Server Data", "làm mới cache và tự động tải lại dữ liệu khi mutation.", [
        ("SIO-REACT-TANSTACK-USEQUERY", "Fetch Server Data with TanStack useQuery Hook", "tải dữ liệu bất đồng bộ và tự động cache bằng useQuery."),
        ("SIO-REACT-USEMUTATION-CACHE-INVALIDATE", "Mutate Server Data and Invalidate Cache Keys", "gửi dữ liệu cập nhật bằng useMutation và xoá cache bằng invalidateQueries."),
        ("SIO-REACT-STALE-WHILE-REVALIDATE", "Configure Stale Time and Cache Expiration Rules", "cấu hình thời gian staleTime và cacheTime cho dữ liệu.")
    ]),
    ("UI_STYLING_SOLUTIONS", "UI Component Styling Architecture", "UI_STYLING_SOLUTIONS_COMPONENTS", "CSS Modules, CSS-in-JS & Utility Styling", "Định cách giao diện bằng Tailwind CSS, CSS Modules, Styled Components hoặc Emotion.", "Tailwind CSS, CSS Modules, Styled Components, Emotion, Shadcn UI, CSS-in-JS", "ULO-UI-STYLING-SOLUTIONS", "Master UI Component Styling and Design System Integration", "áp dụng các giải pháp styling giao diện hiện đại.", "CIO-DESIGN-SYSTEM-THEMING", "Integrate Theme Tokens and Responsive Style Utilities", "tích hợp thiết kế hệ thống theme token và responsive.", [
        ("SIO-REACT-TAILWIND-UTILITY-CLASSES", "Style Components with Tailwind CSS Utility Classes", "định phong cách giao diện bằng các lớp tiện ích Tailwind CSS."),
        ("SIO-REACT-CSS-MODULES-SCOPED", "Scope Component Styles with CSS Modules", "cách ly style riêng cho component bằng CSS Modules."),
        ("SIO-REACT-STYLED-COMPONENTS-THEME", "Build Dynamic Styled Components with ThemeProvider", "tạo linh kiện giao diện động bằng Styled Components và ThemeProvider.")
    ]),
    ("SERVER_SIDE_RENDERING_NEXTJS", "Server-Side Rendering & App Router", "SERVER_SIDE_RENDERING_HYDRATION", "Server-Side Rendering & Client Hydration", "Render giao diện từ máy chủ Server-Side Rendering (SSR), Static Site Generation (SSG) và Next.js.", "Next.js, App Router, SSR, SSG, Server Components, Client Components, Hydration", "ULO-SERVER-SIDE-RENDERING", "Master Server-Side Rendering and Client Hydration", "xây dựng ứng dụng render từ phía server SSR/SSG.", "CIO-SERVER-CLIENT-BOUNDARIES", "Isolate Server and Client Component Execution Boundaries", "phân rã ranh giới giữa Server Components và Client Components.", [
        ("SIO-REACT-NEXTJS-APP-ROUTER-PAGES", "Structure Layouts with Next.js App Router", "tổ chức trang và layout bằng Next.js App Router."),
        ("SIO-REACT-SERVER-VS-CLIENT-COMPONENTS", "Separate React Server Components from Client Components", "phân biệt và sử dụng cờ 'use client' cho Client Components."),
        ("SIO-REACT-SSR-SSG-DATA-FETCHING", "Fetch Static and Dynamic Server Data in Next.js", "tải dữ liệu render tĩnh (SSG) và render động (SSR) trong Next.js.")
    ]),
    ("TESTING_REACT_COMPONENTS", "Automated Component Testing Suites", "COMPONENT_TESTING_ASSERTIONS", "Component Unit Testing & User Event Simulation", "Kiểm thử tự động linh kiện UI bằng React Testing Library và Vitest.", "React Testing Library, Jest, Vitest, screen, fireEvent, userEvent, render", "ULO-COMPONENT-TESTING", "Master Component Unit Testing and User Event Simulation", "viết bài kiểm thử tự động cho linh kiện giao diện.", "CIO-USER-INTERACTION-ASSERTION", "Simulate User Events and Assert DOM State Changes", "giả lập sự kiện người dùng và kiểm tra cây DOM.", [
        ("SIO-REACT-TESTING-LIBRARY-RENDER", "Render Components with React Testing Library", "render linh kiện trong môi trường test bằng React Testing Library."),
        ("SIO-REACT-FIRE-EVENT-SIMULATION", "Simulate User Clicks and Typing with userEvent", "giả lập thao tác click và gõ phím của người dùng bằng userEvent."),
        ("SIO-REACT-SCREEN-QUERY-ASSERT", "Query DOM Nodes with getByText and findByRole", "truy vấn node DOM bằng screen.getByRole và kiểm tra kết quả.")
    ]),
    ("PORTALS_REFS_UNCONTROLLED", "Portals, Refs & Imperative Handlers", "PORTALS_REFS_DOM_ESCAPE", "DOM Escapes & Imperative Ref Handles", "Thao tác DOM trực tiếp qua useRef, forwardRef, useImperativeHandle và ReactDOM.createPortal.", "useRef, forwardRef, useImperativeHandle, createPortal, Modal, DOM escape", "ULO-PORTALS-REFS", "Master DOM Escape Hatches, Refs and Portals", "làm chủ thao tác DOM trực tiếp qua Refs và Portals.", "CIO-IMPERATIVE-DOM-MUTATION", "Mutate DOM Nodes Imperatively via Refs", "thao tác trên node DOM thực tế qua useRef.", [
        ("SIO-REACT-USEREF-DOM-NODE", "Access Native DOM Nodes with useRef Hook", "lấy tham chiếu node DOM thực tế bằng useRef Hook."),
        ("SIO-REACT-FORWARDREF-PARENT-PASS", "Pass Refs to Child Components with forwardRef", "chuyển tiếp ref xuống component con bằng forwardRef."),
        ("SIO-REACT-CREATE-PORTAL-MODAL", "Render Modal Overlay Dialogs via createPortal", "render giao diện Modal đè lên body bằng ReactDOM.createPortal().")
    ]),
    ("ERROR_BOUNDARIES_RESILIENCE", "Error Boundaries & Application Resilience", "ERROR_BOUNDARIES_FALLBACK", "Error Boundaries & Fallback UI Components", "Bắt lỗi hệ thống render bằng Error Boundaries và hiển thị màn hình khắc phục khẩn cấp.", "ErrorBoundary, componentDidCatch, getDerivedStateFromError, fallback UI", "ULO-ERROR-BOUNDARIES", "Master Error Boundaries and Fallback UI Rendering", "khoanh vùng và bắt lỗi crash giao diện bằng Error Boundaries.", "CIO-CRASH-ISOLATION-FALLBACK", "Isolate Rendering Crashes with Fallback Components", "hiển thị giao diện fallback khi linh kiện con bị lỗi.", [
        ("SIO-REACT-ERROR-BOUNDARY-CLASS", "Implement Class-based Error Boundaries", "viết Error Boundary class lắng nghe getDerivedStateFromError."),
        ("SIO-REACT-FALLBACK-UI-RENDER", "Render Custom Fallback UI Components on Crash", "hiển thị giao diện thông báo lỗi custom cho người dùng."),
        ("SIO-REACT-RESET-ERROR-STATE", "Reset Error Boundary State on Navigation", "khôi phục trạng thái Error Boundary khi người dùng chuyển trang.")
    ]),
    ("SUSPENSE_CONCURRENT_FEATURES", "Suspense & Concurrent React Architecture", "SUSPENSE_CONCURRENT_RENDERING", "Concurrent Rendering & Suspense Transitions", "Cơ chế render đồng thời Concurrent Mode, useTransition, useDeferredValue và Suspense.", "Suspense, useTransition, useDeferredValue, Concurrent Mode, non-blocking rendering", "ULO-SUSPENSE-CONCURRENT", "Master Concurrent Rendering and Suspense Transitions", "làm chủ chế độ render đồng thời Concurrent React.", "CIO-NON-BLOCKING-UI-UPDATES", "Prioritize Non-blocking UI State Transitions", "ưu tiên các cập nhật giao diện không gây mượt hình.", [
        ("SIO-REACT-SUSPENSE-ASYNC-BOUNDARY", "Wrap Async Data Components with Suspense", "bọc các linh kiện tải dữ liệu bằng React.Suspense fallback."),
        ("SIO-REACT-USETRANSITION-PRIORITY", "Mark Non-Urgent Updates with useTransition", "đánh dấu cập nhật trạng thái thứ cấp bằng useTransition Hook."),
        ("SIO-REACT-USEDEFERREDVALUE-DEBOUNCE", "Defer High-Frequency Inputs via useDeferredValue", "hoãn cập nhật giá trị biến tần suất cao bằng useDeferredValue.")
    ]),
    ("MICRO_FRONTENDS_FEDERATION", "Micro-Frontends & Module Federation", "MICRO_FRONTEND_MODULE_FEDERATION", "Micro-Frontend Architectures & Module Sharing", "Phân rã ứng dụng web lớn thành các micro-frontends chạy độc lập qua Module Federation.", "Micro-Frontends, Module Federation, Webpack, Single-SPA, independent deployment", "ULO-MICRO-FRONTENDS", "Master Micro-Frontend Architectures and Module Federation", "phân rã ứng dụng web thành kiến trúc Micro-Frontends.", "CIO-REMOTE-MODULE-INTEGRATION", "Integrate Remote Federated Modules dynamically", "nạp và tích hợp các module từ xa động.", [
        ("SIO-REACT-MODULE-FEDERATION-HOST", "Expose Host App Containers for Remote Modules", "cấu hình ứng dụng Host nhận các module từ xa qua Module Federation."),
        ("SIO-REACT-REMOTE-COMPONENT-IMPORT", "Import Dynamically Federated Components", "nạp linh kiện từ xa bằng dynamic import và React.lazy."),
        ("SIO-REACT-SINGLE-SPA-ROUTING", "Orchestrate Micro-Frontend Apps via Single-SPA", "điều phối các ứng dụng con bằng khung Single-SPA.")
    ]),
    ("ACCESSIBILITY_A11Y_PATTERNS", "Web Accessibility (a11y) Architecture", "ACCESSIBILITY_A11Y_PATTERNS", "Accessible ARIA Roles & Keyboard Focus", "Xây dựng giao diện hỗ trợ người khuyết tật (a11y), tiêu chuẩn WCAG, ARIA roles và bàn phím.", "a11y, ARIA roles, aria-expanded, screen readers, focus management, WCAG", "ULO-ACCESSIBILITY-A11Y", "Master Web Accessibility (a11y) and ARIA Specifications", "xây dựng giao diện đạt chuẩn tiếp cận a11y (WCAG).", "CIO-KEYBOARD-FOCUS-NAVIGATION", "Manage Keyboard Focus Traps and Accessible Roles", "quản lý phím Tab và nhãn điều khiển màn hình đọc.", [
        ("SIO-REACT-ARIA-ATTRIBUTES-ROLES", "Annotate Accessible Elements with ARIA Attributes", "gán thuộc tính role, aria-label, aria-expanded cho linh kiện."),
        ("SIO-REACT-KEYBOARD-FOCUS-TRAP", "Implement Keyboard Focus Traps in Modals", "quản lý con trỏ bàn phím không thoát khỏi Modal bằng Focus Trap."),
        ("SIO-REACT-SCREEN-READER-ANNOUNCE", "Announce Dynamic Updates to Screen Readers", "thông báo nội dung cập nhật động cho phần mềm đọc màn hình.")
    ]),
    ("STATE_MACHINE_COMPOSABLE_LOGIC", "Finite State Machines & Logic Engines", "FINITE_STATE_MACHINES", "Finite State Machines & Declarative Transitions", "Mô hình hóa trạng thái phức tạp với Finite State Machines (XState).", "XState, state machines, statechart, transitions, deterministic logic", "ULO-FINITE-STATE-MACHINES", "Master Finite State Machines and Declarative Transitions", "mô hình hóa logic ứng dụng bằng máy trạng thái hữu hạn.", "CIO-DETERMINISTIC-STATE-CHART", "Map Deterministic Transitions in Statecharts", "khai báo các trạng thái và sự kiện chuyển đổi định sẵn.", [
        ("SIO-REACT-XSTATE-MACHINE-SETUP", "Create Finite State Machines with XState", "khai báo máy trạng thái XState với createMachine."),
        ("SIO-REACT-USEMACHINE-HOOK-INTEGRATION", "Connect State Machines to Components via useMachine", "kết nối máy trạng thái với linh kiện bằng useMachine Hook."),
        ("SIO-REACT-PREVENT-INVALID-STATES", "Prevent Invalid UI Transitions with Statechart Rules", "ngăn chặn trạng thái bất hợp lý bằng quy tắc chuyển đổi statechart.")
    ])
]

def main():
    print("🚀 Building roadmap_sh_react with 18 Neutral Concepts & 90 LOs...")
    build_proj("roadmap_sh_react", react_items)

if __name__ == "__main__":
    main()
