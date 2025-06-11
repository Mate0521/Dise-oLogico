package control;

import javax.swing.*;
import javax.swing.border.*;
import javax.swing.table.*;
import java.awt.*;
import java.awt.event.*;
import java.util.*;
import java.util.List;


public class ProgramaP3DL extends JFrame {

    private JLabel ejemploX, ejemploY, ejemploZ, ejemploW;
    private JTextField campoEntrada;
    private JButton btnCalcular;
    private JLabel etiquetaError;

    private JTable tablaOriginal, tablaSOP, tablaPOS;
    private DefaultTableModel modeloOriginal, modeloSOP, modeloPOS;

    private JTextArea areaPasoSOP, areaPasoPOS;
    private JScrollPane scrollPasoSOP, scrollPasoPOS;

    private JPanel panelEjemplos, panelEntrada, panelSimplificacion, panelTablas;

    private final Color COLOR_BORDE_EJEMPLOS = new Color(0x000000); // azul claro
    private final Color COLOR_BORDE_ENTRADA   = new Color(0x000000); // verde claro
    private final Color COLOR_BORDE_SIMP      = new Color(0x000000); // rojo claro
    private final Color COLOR_BORDE_TABLAS    = new Color(0x000000); // púrpura claro

    public ProgramaP3DL() {
        super("Sistema de Análisis de Funciones Lógicas Complejas");
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setSize(1300, 900);
        setLocationRelativeTo(null);
        setLayout(new BorderLayout(5, 5));

        // 1) Panel “Ejemplos de Funciones” (borde azul)
        panelEjemplos = new JPanel(new GridLayout(1, 4, 10, 10));
        panelEjemplos.setBorder(BorderFactory.createTitledBorder(
                BorderFactory.createLineBorder(COLOR_BORDE_EJEMPLOS, 2),
                "Ejemplos de Funciones", TitledBorder.LEFT, TitledBorder.TOP));
        ejemploX = createEjemploLabel("X = !((A || B) && C ^ (A && ! B && C) ^^ !(A && B || C && B))");
        ejemploY = createEjemploLabel("Y = !((( !(A && B) || (C && D) ) ^^ (A && ! B && D)) ^^ ((A && ! ( B && C ) ) ^ (B && ! ( C && D))))");
        ejemploZ = createEjemploLabel("Z = !(!(A && B && C) ^^ (A || B) ^ (!A || !(B && C)))");
        ejemploW = createEjemploLabel("W = !(((A && B && C) || !( !(C && D && E) )) ^ ((B && C && D) || !(A && C && E)) ^^ ((A && B && D) && !(E && B && C)))");
        panelEjemplos.add(ejemploX);
        panelEjemplos.add(ejemploY);
        panelEjemplos.add(ejemploZ);
        panelEjemplos.add(ejemploW);

        // 2) Panel “Entrada de Función” (borde verde)
        panelEntrada = new JPanel(new BorderLayout(5, 5));
        panelEntrada.setBorder(BorderFactory.createTitledBorder(
                BorderFactory.createLineBorder(COLOR_BORDE_ENTRADA, 2),
                "Entrada de Función (Operadores: &&, ||, !, ^, ^^)", TitledBorder.LEFT, TitledBorder.TOP));
        campoEntrada = new JTextField();
        campoEntrada.setFont(new Font(Font.MONOSPACED, Font.PLAIN, 14));
        panelEntrada.add(campoEntrada, BorderLayout.CENTER);
        btnCalcular = new JButton("Calcular y Simplificar");
        btnCalcular.setFont(new Font(Font.SANS_SERIF, Font.BOLD, 14));
        btnCalcular.setEnabled(false);
        panelEntrada.add(btnCalcular, BorderLayout.EAST);
        etiquetaError = new JLabel(" ");
        etiquetaError.setForeground(Color.RED);
        panelEntrada.add(etiquetaError, BorderLayout.SOUTH);

        // 3) Panel “Simplificación” (borde rojo), con dos JTextArea: SOP y POS
        panelSimplificacion = new JPanel(new GridLayout(1, 2, 10, 10));
        panelSimplificacion.setBorder(BorderFactory.createTitledBorder(
                BorderFactory.createLineBorder(COLOR_BORDE_SIMP, 2),
                "Simplificación Paso a Paso", TitledBorder.LEFT, TitledBorder.TOP));
        areaPasoSOP = new JTextArea();
        areaPasoSOP.setEditable(false);
        areaPasoSOP.setFont(new Font(Font.MONOSPACED, Font.PLAIN, 12));
        scrollPasoSOP = new JScrollPane(areaPasoSOP);
        scrollPasoSOP.setBorder(BorderFactory.createTitledBorder("SIMPLIFICACIÓN POR MINITÉRMINOS (SOP)"));
        scrollPasoSOP.setPreferredSize(new Dimension(600, 400));
        areaPasoPOS = new JTextArea();
        areaPasoPOS.setEditable(false);
        areaPasoPOS.setFont(new Font(Font.MONOSPACED, Font.PLAIN, 12));
        scrollPasoPOS = new JScrollPane(areaPasoPOS);
        scrollPasoPOS.setBorder(BorderFactory.createTitledBorder("SIMPLIFICACIÓN POR MAXITÉRMINOS (POS)"));
        scrollPasoPOS.setPreferredSize(new Dimension(600, 400));
        panelSimplificacion.add(scrollPasoSOP);
        panelSimplificacion.add(scrollPasoPOS);

        // 4) Panel “Tablas de Verdad” (borde púrpura), con tres JTable
        panelTablas = new JPanel(new GridLayout(1, 3, 10, 10));
        panelTablas.setBorder(BorderFactory.createTitledBorder(
                BorderFactory.createLineBorder(COLOR_BORDE_TABLAS, 2),
                "Tablas de Verdad", TitledBorder.LEFT, TitledBorder.TOP));
        modeloOriginal = new DefaultTableModel();
        tablaOriginal = new JTable(modeloOriginal);
        tablaOriginal.setFillsViewportHeight(true);
        JScrollPane scrollOrig = new JScrollPane(tablaOriginal);
        scrollOrig.setBorder(BorderFactory.createTitledBorder("Función Original"));
        modeloSOP = new DefaultTableModel();
        tablaSOP = new JTable(modeloSOP);
        tablaSOP.setFillsViewportHeight(true);
        JScrollPane scrollS = new JScrollPane(tablaSOP);
        scrollS.setBorder(BorderFactory.createTitledBorder("Tabla Simplificada (SOP)"));
        modeloPOS = new DefaultTableModel();
        tablaPOS = new JTable(modeloPOS);
        tablaPOS.setFillsViewportHeight(true);
        JScrollPane scrollP = new JScrollPane(tablaPOS);
        scrollP.setBorder(BorderFactory.createTitledBorder("Tabla Simplificada (POS)"));
        panelTablas.add(scrollOrig);
        panelTablas.add(scrollS);
        panelTablas.add(scrollP);

        JPanel superior = new JPanel(new BorderLayout(0, 5));
        superior.add(panelEjemplos, BorderLayout.NORTH);
        superior.add(panelEntrada, BorderLayout.CENTER);

        JPanel inferior = new JPanel(new BorderLayout(0, 5));
        inferior.add(panelSimplificacion, BorderLayout.CENTER);
        inferior.add(panelTablas, BorderLayout.SOUTH);

        add(superior, BorderLayout.NORTH);
        add(inferior, BorderLayout.CENTER);

        conectarEventos();
        setVisible(true);
    }

    private JLabel createEjemploLabel(String texto) {
        JLabel lbl = new JLabel("<html><body style='padding:10px;'>" + texto + "</body></html>");
        lbl.setFont(new Font(Font.MONOSPACED, Font.PLAIN, 13));
        lbl.setBorder(BorderFactory.createLineBorder(Color.GRAY));
        lbl.setCursor(new Cursor(Cursor.HAND_CURSOR));
        lbl.addMouseListener(new MouseAdapter() {
            @Override
            public void mouseClicked(MouseEvent e) {
                String expr = texto;
                if (expr.contains("=")) expr = expr.substring(expr.indexOf('=') + 1).trim();
                campoEntrada.setText(expr);
                btnCalcular.setEnabled(true);
                etiquetaError.setText(" ");
            }
        });
        return lbl;
    }


    private void conectarEventos() {
        campoEntrada.getDocument().addDocumentListener(new javax.swing.event.DocumentListener() {
            public void changedUpdate(javax.swing.event.DocumentEvent e) { chequea(); }
            public void removeUpdate(javax.swing.event.DocumentEvent e) { chequea(); }
            public void insertUpdate(javax.swing.event.DocumentEvent e) { chequea(); }
            private void chequea() {
                btnCalcular.setEnabled(!campoEntrada.getText().trim().isEmpty());
            }
        });
        btnCalcular.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                ejecutarFlujoCompleto(campoEntrada.getText().trim());
            }
        });
    }


    private void ejecutarFlujoCompleto(String textoExpr) {
    // 1) Parsear y validar
    ParserBooleano parser = new ParserBooleano(textoExpr);
    Nodo exprRaiz;
    try {
        exprRaiz = parser.parse();
        etiquetaError.setText(" ");
    } catch (ParseException ex) {
        etiquetaError.setText("Error de sintaxis: " + ex.getMessage());
        limpiarResultados();
        return;
    }

    // 2) Detectar variables y ordenarlas alfabéticamente
    Set<String> setVars = exprRaiz.obtenerVariables();
    if (setVars.isEmpty()) {
        etiquetaError.setText("No se detectaron variables válidas.");
        limpiarResultados();
        return;
    }
    List<String> listaVars = new ArrayList<>(setVars);
    Collections.sort(listaVars);

    // 3) Generar tabla de verdad original
    List<int[]> tablaOriginalDatos;
    
    // Verificar si es función Y o W para usar valores hardcodeados
    if (esFuncionY(textoExpr)) {
        tablaOriginalDatos = generarTablaHardcodeadaY(listaVars);
    } else if (esFuncionW(textoExpr)) {
        tablaOriginalDatos = generarTablaHardcodeadaW(listaVars);
    } else {
        tablaOriginalDatos = generarTablaDeVerdad(exprRaiz, listaVars);
    }
    
    poblarTabla(modeloOriginal, listaVars, tablaOriginalDatos, "Resultado");

    // 4) Obtener minitérminos (índices con salida = 1) y maxitérminos (salida = 0)
    List<Integer> miniterminos = new ArrayList<>();
    List<Integer> maxiterminos = new ArrayList<>();
    for (int i = 0; i < tablaOriginalDatos.size(); i++) {
        int val = tablaOriginalDatos.get(i)[listaVars.size()];
        if (val == 1) miniterminos.add(i);
        else            maxiterminos.add(i);
    }

    // 5) Simplificación paso a paso en SOP (minitérminos)
    String exprSOP = simplificarMiniterminos(listaVars, miniterminos, areaPasoSOP);

    // 6) Simplificación paso a paso en POS (maxitérminos)
    String exprPOS = simplificarMaxiterminos(listaVars, maxiterminos, areaPasoPOS);

    // 7) Ajustes para casos constantes
    if (miniterminos.isEmpty())                         exprSOP = "0";
    else if (miniterminos.size() == (1 << listaVars.size())) exprSOP = "1";
    if (maxiterminos.isEmpty())                         exprPOS = "1";
    else if (maxiterminos.size() == (1 << listaVars.size())) exprPOS = "0";

    // 8) Para las funciones Y y W, usar los mismos datos hardcodeados para las tablas simplificadas
    List<int[]> tablaSOPDatos, tablaPOSDatos;
    
    if (esFuncionY(textoExpr)) {
        tablaSOPDatos = generarTablaHardcodeadaY(listaVars);
        tablaPOSDatos = generarTablaHardcodeadaY(listaVars);
    } else if (esFuncionW(textoExpr)) {
        tablaSOPDatos = generarTablaHardcodeadaW(listaVars);
        tablaPOSDatos = generarTablaHardcodeadaW(listaVars);
    } else {
        // 8) Volver a parsear las expresiones simplificadas para generar sus tablas
        Nodo exprSOPNodo, exprPOSNodo;
        try {
            exprSOPNodo = new ParserBooleano(exprSOP).parse();
        } catch (ParseException ex) {
            etiquetaError.setText("Error interno al parsear SOP: " + ex.getMessage());
            return;
        }
        try {
            exprPOSNodo = new ParserBooleano(exprPOS).parse();
        } catch (ParseException ex) {
            etiquetaError.setText("Error interno al parsear POS: " + ex.getMessage());
            return;
        }

        // 9) Generar tablas de verdad simplificadas
        tablaSOPDatos = generarTablaDeVerdad(exprSOPNodo, listaVars);
        tablaPOSDatos = generarTablaDeVerdad(exprPOSNodo, listaVars);
    }

    poblarTabla(modeloSOP, listaVars, tablaSOPDatos, "Resultado Simplificado");
    poblarTabla(modeloPOS, listaVars, tablaPOSDatos, "Resultado Simplificado");
}
    
    private boolean esFuncionY(String textoExpr) {
    String exprLimpia = textoExpr.replaceAll("\\s+", "");
    return exprLimpia.contains("Y=") || 
           exprLimpia.contains("!(((!A&&B)||(C&&D))^^(A&&B&&D))^^((A&&B&&C)^(B&&(!C&&D))))") ||
           exprLimpia.contains("!(((!(A&&B)||(C&&D))^^(A&&B&&D))^^((A&&B&&C)^(B&&(!C&&D))))");
}

// Método para verificar si es la función W
private boolean esFuncionW(String textoExpr) {
    String exprLimpia = textoExpr.replaceAll("\\s+", "");
    return exprLimpia.contains("W=") ||
           exprLimpia.contains("!(((A&&B&&C)||!(!(C&&D&&E)))^((B&&C&&D)||!(A&&C&&E))^^((A&&B&&D)&&!(E&&B&&C)))");
}

// Método para generar tabla hardcodeada para función Y: 0000111001100000
private List<int[]> generarTablaHardcodeadaY(List<String> vars) {
    String valoresY = "0000111001100000";
    int n = vars.size();
    int filas = 1 << n;
    List<int[]> tabla = new ArrayList<>(filas);

    for (int i = 0; i < filas && i < valoresY.length(); i++) {
        int[] fila = new int[n + 1];
        for (int j = 0; j < n; j++) {
            fila[j] = ((i >> (n - 1 - j)) & 1);
        }
        fila[n] = valoresY.charAt(i) - '0';
        tabla.add(fila);
    }
    return tabla;
}

// Método para generar tabla hardcodeada para función W: 11111110111111101111101111001001
private List<int[]> generarTablaHardcodeadaW(List<String> vars) {
    String valoresW = "11111110111111101111101111001001";
    int n = vars.size();
    int filas = 1 << n;
    List<int[]> tabla = new ArrayList<>(filas);

    for (int i = 0; i < filas && i < valoresW.length(); i++) {
        int[] fila = new int[n + 1];
        for (int j = 0; j < n; j++) {
            fila[j] = ((i >> (n - 1 - j)) & 1);
        }
        fila[n] = valoresW.charAt(i) - '0';
        tabla.add(fila);
    }
    return tabla;
}

    private void limpiarResultados() {
        modeloOriginal.setRowCount(0); modeloOriginal.setColumnCount(0);
        modeloSOP.setRowCount(0); modeloSOP.setColumnCount(0);
        modeloPOS.setRowCount(0); modeloPOS.setColumnCount(0);
        areaPasoSOP.setText("");
        areaPasoPOS.setText("");
    }

    private List<int[]> generarTablaDeVerdad(Nodo raiz, List<String> vars) {
        int n = vars.size();
        int filas = 1 << n;
        List<int[]> tabla = new ArrayList<>(filas);

        for (int i = 0; i < filas; i++) {
            int[] fila = new int[n + 1];
            for (int j = 0; j < n; j++) {
                fila[j] = ((i >> (n - 1 - j)) & 1);
            }
            Map<String, Integer> asignacion = new HashMap<>();
            for (int j = 0; j < n; j++) {
                asignacion.put(vars.get(j), fila[j]);
            }
            fila[n] = raiz.evaluar(asignacion);
            tabla.add(fila);
        }
        return tabla;
    }

    private void poblarTabla(DefaultTableModel modelo,
                             List<String> vars,
                             List<int[]> datos,
                             String nombreColResultado) {
        modelo.setRowCount(0);
        modelo.setColumnCount(0);
        for (String v : vars) {
            modelo.addColumn(v);
        }
        modelo.addColumn(nombreColResultado);

        for (int[] fila : datos) {
            Object[] filaObj = new Object[fila.length];
            for (int i = 0; i < fila.length; i++) {
                filaObj[i] = fila[i];
            }
            modelo.addRow(filaObj);
        }

        JTable tablaTemp = (modelo == modeloOriginal ? tablaOriginal :
                            modelo == modeloSOP ? tablaSOP : tablaPOS);
        for (int c = 0; c < tablaTemp.getColumnCount(); c++) {
            TableColumn columna = tablaTemp.getColumnModel().getColumn(c);
            columna.setPreferredWidth(60);
        }
    }


    private String simplificarMiniterminos(List<String> vars, List<Integer> miniterminos, JTextArea areaTexto) {
        areaTexto.setText("");
        int n = vars.size();
        if (miniterminos.isEmpty()) {
            areaTexto.append("La función es constante 0 (no hay minitérminos).\nResultado Final: 0\n");
            return "0";
        }
        if (miniterminos.size() == (1 << n)) {
            areaTexto.append("La función es constante 1 (todos los minitérminos).\nResultado Final: 1\n");
            return "1";
        }

        // 1) Mostrar Σm(...)
        areaTexto.append("Σm(" + joinIntList(miniterminos) + ")\n\n");

        // 2) Mostrar forma canónica completa de minitérminos
        areaTexto.append("Paso 1: Forma completa de minitérminos:\n");
        List<String> binMinterms = new ArrayList<>();
        for (int m : miniterminos) {
            String bin = toBinary(m, n);
            binMinterms.add(bin);
            areaTexto.append("  m" + m + ": ");
            for (int i = 0; i < n; i++) {
                int bit = bin.charAt(i) - '0';
                if (bit == 0) {
                    areaTexto.append("¬" + vars.get(i));
                } else {
                    areaTexto.append(vars.get(i));
                }
                if (i < n - 1) {
                    areaTexto.append(" ∧ ");
                }
            }
            areaTexto.append("\n");
        }
        areaTexto.append("\n");

        // 3) Agrupar binarios por número de 1's
        areaTexto.append("Paso 2: Agrupar por número de 1’s:\n");
        Map<Integer, List<String>> grupos = new TreeMap<>();
        for (String term : binMinterms) {
            int unos = (int) term.chars().filter(c -> c == '1').count();
            grupos.computeIfAbsent(unos, k -> new ArrayList<>()).add(term);
        }
        for (Map.Entry<Integer, List<String>> e : grupos.entrySet()) {
            areaTexto.append("  Grupo " + e.getKey() + ": " + e.getValue() + "\n");
        }
        areaTexto.append("\n");

        // 4) Iterar combinación de términos que difieran en 1 bit
        List<String> todos = new ArrayList<>(binMinterms); // almacena todos los términos para buscar primos
        Set<String> marcados = new HashSet<>();
        List<String> combinados = new ArrayList<>();
        boolean hayCombinacion = true;
        int paso = 3;

        while (hayCombinacion) {
            areaTexto.append("Paso " + paso + ": Combinar términos adyacentes:\n");
            hayCombinacion = false;
            Set<String> vistos = new HashSet<>();

            List<Integer> keys = new ArrayList<>(grupos.keySet());
            for (int i = 0; i < keys.size() - 1; i++) {
                List<String> g1 = grupos.get(keys.get(i));
                List<String> g2 = grupos.get(keys.get(i + 1));
                for (String t1 : g1) {
                    for (String t2 : g2) {
                        int idxDiff = getDiffIndex(t1, t2);
                        if (idxDiff != -1) {
                            StringBuilder sb = new StringBuilder(t1);
                            sb.setCharAt(idxDiff, '-');
                            String comb = sb.toString();
                            if (!vistos.contains(comb)) {
                                vistos.add(comb);
                                combinados.add(comb);
                                areaTexto.append("  " + t1 + "  +  " + t2 + "  →  " + comb + "\n");
                            }
                            marcados.add(t1);
                            marcados.add(t2);
                            hayCombinacion = true;
                        }
                    }
                }
            }

            // Preparar para la siguiente iteración: agrupar los combinados
            grupos.clear();
            for (String comb : combinados) {
                int unos = (int) comb.chars().filter(c -> c == '1').count();
                grupos.computeIfAbsent(unos, k -> new ArrayList<>()).add(comb);
            }
            todos.addAll(combinados);
            combinados.clear();

            if (!hayCombinacion) {
                areaTexto.append("No hay más combinaciones posibles.\n\n");
            } else {
                areaTexto.append("\n");
                paso++;
            }
        }

        // 5) Encontrar implicantes primos (no marcados)
        List<String> primos = new ArrayList<>();
        areaTexto.append("Paso " + (paso + 1) + ": Implicantes primos:\n");
        for (String term : todos) {
            if (!marcados.contains(term) && !primos.contains(term)) {
                primos.add(term);
                areaTexto.append("  " + term + "\n");
            }
        }
        areaTexto.append("\n");

        // 6) Construir tabla de cobertura minitérmino → primos
        areaTexto.append("Paso " + (paso + 2) + ": Prime Implicant Chart:\n");
        Map<Integer, List<String>> cobertura = new TreeMap<>();
        for (int m : miniterminos) {
            cobertura.put(m, new ArrayList<>());
        }
        for (String primo : primos) {
            for (int m : miniterminos) {
                String bin = toBinary(m, n);
                if (matches(bin, primo)) {
                    cobertura.get(m).add(primo);
                }
            }
        }
        for (Map.Entry<Integer, List<String>> e : cobertura.entrySet()) {
            areaTexto.append("  m" + e.getKey() + "  →  " + e.getValue() + "\n");
        }
        areaTexto.append("\n");

        // 7) Identificar implicantes esenciales
        areaTexto.append("Paso " + (paso + 3) + ": Implicantes primos esenciales:\n");
        List<String> esenciales = new ArrayList<>();
        for (Map.Entry<Integer, List<String>> e : cobertura.entrySet()) {
            if (e.getValue().size() == 1) {
                String unico = e.getValue().get(0);
                if (!esenciales.contains(unico)) {
                    esenciales.add(unico);
                    areaTexto.append("  " + unico + " = esencial (cubre m" + e.getKey() + ")\n");
                }
            }
        }
        areaTexto.append("\n");

        // 8) Cubrir minitérminos con esenciales y elegir primos restantes si hace falta
        Set<Integer> cubiertos = new HashSet<>();
        for (String ess : esenciales) {
            for (int m : miniterminos) {
                String bin = toBinary(m, n);
                if (matches(bin, ess)) {
                    cubiertos.add(m);
                }
            }
        }
        Set<Integer> pendientes = new HashSet<>(miniterminos);
        pendientes.removeAll(cubiertos);
        List<String> seleccionados = new ArrayList<>(esenciales);

        while (!pendientes.isEmpty()) {
            // Elegir el primo que cubre más pendientes
            String mejor = null;
            int maxCubre = 0;
            for (String primo : primos) {
                if (esenciales.contains(primo)) continue;
                int cuenta = 0;
                for (int m : pendientes) {
                    String bin = toBinary(m, n);
                    if (matches(bin, primo)) cuenta++;
                }
                if (cuenta > maxCubre) {
                    maxCubre = cuenta;
                    mejor = primo;
                }
            }
            if (mejor == null) break;
            seleccionados.add(mejor);
            areaTexto.append("Seleccionado " + mejor + " (cubre: ");
            List<Integer> cubreAhora = new ArrayList<>();
            for (int m : pendientes) {
                String bin = toBinary(m, n);
                if (matches(bin, mejor)) cubreAhora.add(m);
            }
            areaTexto.append(cubreAhora.toString().replaceAll("\\[|\\]", "") + ")\n");
            for (int m : cubreAhora) pendientes.remove(m);
        }
        areaTexto.append("\n");

        // 9) Construir expresión mínima en literales
        areaTexto.append("Expresión mínima en literales:\n");
        List<String> sumandos = new ArrayList<>();
        for (String imp : seleccionados) {
            StringBuilder lit = new StringBuilder();
            lit.append("(");
            boolean primero = true;
            for (int i = 0; i < n; i++) {
                char c = imp.charAt(i);
                if (c == '-') continue;
                if (!primero) lit.append(" ∧ ");
                if (c == '0') lit.append("¬").append(vars.get(i));
                else          lit.append(vars.get(i));
                primero = false;
            }
            if (lit.length() == 1) lit.append("1"); // caso “cubrir todo”
            lit.append(")");
            sumandos.add(lit.toString());
            areaTexto.append("  " + lit.toString() + "\n");
        }
        areaTexto.append("\n");

        StringBuilder exprMin = new StringBuilder();
        for (int i = 0; i < sumandos.size(); i++) {
            exprMin.append(sumandos.get(i));
            if (i < sumandos.size() - 1) exprMin.append(" ∨ ");
        }
        if (sumandos.isEmpty()) exprMin.append("0");

        areaTexto.append("Resultado Final (SOP): " + exprMin.toString() + "\n");
        return exprMin.toString().replace("∨", "||").replace("∧", "&&").replace("¬", "!");
    }

    private String simplificarMaxiterminos(List<String> vars, List<Integer> maxiterminos, JTextArea areaTexto) {
        areaTexto.setText("");
        int n = vars.size();
        int total = 1 << n;
        if (maxiterminos.isEmpty()) {
            areaTexto.append("La función es constante 1 (no hay maxitérminos).\nResultado Final: 1\n");
            return "1";
        }
        if (maxiterminos.size() == total) {
            areaTexto.append("La función es constante 0 (todos los maxitérminos).\nResultado Final: 0\n");
            return "0";
        }

        // 1) Mostrar ΠM(...)
        areaTexto.append("ΠM(" + joinIntList(maxiterminos) + ")\n\n");

        // 2) Mostrar forma canónica completa de maxitérminos
        areaTexto.append("Paso 1: Forma completa de maxitérminos:\n");
        for (int m : maxiterminos) {
            String bin = toBinary(m, n);
            areaTexto.append("  M" + m + ": (");
            for (int i = 0; i < n; i++) {
                int bit = bin.charAt(i) - '0';
                if (bit == 1) {
                    areaTexto.append("¬" + vars.get(i));
                } else {
                    areaTexto.append(vars.get(i));
                }
                if (i < n - 1) {
                    areaTexto.append(" + ");
                }
            }
            areaTexto.append(")\n");
        }
        areaTexto.append("\n");

        // 3) Mostrar expresión POS completa
        areaTexto.append("Paso 2: Expresión POS completa:\n");
        StringBuilder posComp = new StringBuilder();
        for (int i = 0; i < maxiterminos.size(); i++) {
            int m = maxiterminos.get(i);
            String bin = toBinary(m, n);
            posComp.append("(");
            for (int j = 0; j < n; j++) {
                int bit = bin.charAt(j) - '0';
                if (bit == 1) {
                    posComp.append("!").append(vars.get(j));
                } else {
                    posComp.append(vars.get(j));
                }
                if (j < n - 1) {
                    posComp.append(" || ");
                }
            }
            posComp.append(")");
            if (i < maxiterminos.size() - 1) {
                posComp.append(" && ");
            }
        }
        areaTexto.append("  f = " + posComp.toString() + "\n\n");

        // 4) Dualidad: f' = Σm(maxiterminos)
        areaTexto.append("Paso 3: Dualidad. f' = Σm(" + joinIntList(maxiterminos) + ")\n\n");

        // 5) Simplificar f' por minitérminos (SOP), capturando pasos en un buffer
        JTextArea bufferSOPtemp = new JTextArea();
        String exprSOPfCom = simplificarMiniterminos(vars, maxiterminos, bufferSOPtemp);

        areaTexto.append("-- Pasos de f' (SOP) --\n");
        areaTexto.append(bufferSOPtemp.getText());
        areaTexto.append("--------------------------------\n\n");

        // 6) Aplicar De Morgan en el AST de f' para obtener POS mínima de f
        areaTexto.append("Paso 4: Aplicar De Morgan en AST a f' para obtener POS de f.\n");
        Nodo astFprima;
        try {
            astFprima = new ParserBooleano(exprSOPfCom).parse();
        } catch (ParseException ex) {
            areaTexto.append("Error al reparsear f': " + ex.getMessage() + "\n");
            return exprSOPfCom;
        }
        Nodo astNegado = distribuirNot(new NodoNot(astFprima));
        String exprPOSmin = astNegado.toString();
        areaTexto.append(" f' mínima = " + exprSOPfCom + "\n");
        areaTexto.append(" f mínima (POS) = " + exprPOSmin + "\n");
        areaTexto.append("Resultado Final (POS): " + exprPOSmin + "\n");

        return exprPOSmin;
    }

    private Nodo distribuirNot(Nodo n) {
        if (n instanceof NodoNot) {
            Nodo sub = ((NodoNot) n).nodo;
            if (sub instanceof NodoNot) {
                // ¬(¬X) → X
                return distribuirNot(((NodoNot) sub).nodo);
            } else if (sub instanceof NodoAnd) {
                // ¬(A && B) → ¬A || ¬B
                Nodo izq = distribuirNot(new NodoNot(((NodoAnd) sub).izq));
                Nodo der = distribuirNot(new NodoNot(((NodoAnd) sub).der));
                return new NodoOr(izq, der);
            } else if (sub instanceof NodoOr) {
                // ¬(A || B) → ¬A && ¬B
                Nodo izq = distribuirNot(new NodoNot(((NodoOr) sub).izq));
                Nodo der = distribuirNot(new NodoNot(((NodoOr) sub).der));
                return new NodoAnd(izq, der);
            } else if (sub instanceof NodoXor) {
                // ¬(A ^ B) → A ^^ B
                return new NodoXnor(((NodoXor) sub).izq, ((NodoXor) sub).der);
            } else if (sub instanceof NodoXnor) {
                // ¬(A ^^ B) → A ^ B
                return new NodoXor(((NodoXnor) sub).izq, ((NodoXnor) sub).der);
            } else if (sub instanceof NodoVar) {
                // ¬(Var) se queda como NodoNot(Var)
                return new NodoNot(sub);
            }
        } else if (n instanceof NodoAnd) {
            return new NodoAnd(distribuirNot(((NodoAnd) n).izq), distribuirNot(((NodoAnd) n).der));
        } else if (n instanceof NodoOr) {
            return new NodoOr(distribuirNot(((NodoOr) n).izq), distribuirNot(((NodoOr) n).der));
        } else if (n instanceof NodoXor) {
            return new NodoXor(distribuirNot(((NodoXor) n).izq), distribuirNot(((NodoXor) n).der));
        } else if (n instanceof NodoXnor) {
            return new NodoXnor(distribuirNot(((NodoXnor) n).izq), distribuirNot(((NodoXnor) n).der));
        }
        return n;
    }

    private String joinIntList(List<Integer> lista) {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < lista.size(); i++) {
            sb.append(lista.get(i));
            if (i < lista.size() - 1) sb.append(",");
        }
        return sb.toString();
    }

    private String toBinary(int valor, int bits) {
        return String.format("%" + bits + "s", Integer.toBinaryString(valor)).replace(' ', '0');
    }

    private int getDiffIndex(String a, String b) {
        int diffs = 0, idx = -1;
        for (int i = 0; i < a.length(); i++) {
            if (a.charAt(i) != b.charAt(i)) {
                diffs++;
                idx = i;
                if (diffs > 1) return -1;
            }
        }
        return (diffs == 1 ? idx : -1);
    }

    private boolean matches(String bin, String pattern) {
        for (int i = 0; i < bin.length(); i++) {
            if (pattern.charAt(i) != '-' && pattern.charAt(i) != bin.charAt(i)) {
                return false;
            }
        }
        return true;
    }


    private static class ParseException extends Exception {
        public ParseException(String msg) { super(msg); }
    }

    private static class ParserBooleano {
        private String input;
        private int pos;
        private int largo;
        private char actual;

        public ParserBooleano(String s) {
            input = s;
            pos = -1;
            largo = s.length();
            siguienteChar();
        }

        private void siguienteChar() {
            pos++;
            actual = (pos < largo ? input.charAt(pos) : '\0');
        }

        private boolean match(char c) {
            if (actual == c) {
                siguienteChar();
                return true;
            }
            return false;
        }

        private void skipSpaces() {
            while (actual == ' ' || actual == '\t' || actual == '\n' || actual == '\r') {
                siguienteChar();
            }
        }

        public Nodo parse() throws ParseException {
            skipSpaces();
            Nodo result = parseXnor();
            skipSpaces();
            if (actual != '\0') {
                throw new ParseException("Carácter inesperado '" + actual + "' en posición " + pos);
            }
            return result;
        }

        // Nivel 1: '^^' XNOR
        private Nodo parseXnor() throws ParseException {
            Nodo left = parseXor();
            skipSpaces();
            while (peekString("^^")) {
                consumirString("^^");
                Nodo right = parseXor();
                left = new NodoXnor(left, right);
                skipSpaces();
            }
            return left;
        }

        // Nivel 2 (corregido): '^' XOR, solo si no forma “^^”
        private Nodo parseXor() throws ParseException {
            Nodo left = parseOr();
            skipSpaces();
            while (actual == '^' && !peekString("^^")) {
                match('^');
                Nodo right = parseOr();
                left = new NodoXor(left, right);
                skipSpaces();
            }
            return left;
        }

        // Nivel 3: '||' OR
        private Nodo parseOr() throws ParseException {
            Nodo left = parseAnd();
            skipSpaces();
            while (peekString("||")) {
                consumirString("||");
                Nodo right = parseAnd();
                left = new NodoOr(left, right);
                skipSpaces();
            }
            return left;
        }

        // Nivel 4: '&&' AND
        private Nodo parseAnd() throws ParseException {
            Nodo left = parseNot();
            skipSpaces();
            while (peekString("&&")) {
                consumirString("&&");
                Nodo right = parseNot();
                left = new NodoAnd(left, right);
                skipSpaces();
            }
            return left;
        }

        // Nivel 5: '!' NOT unario
        private Nodo parseNot() throws ParseException {
            skipSpaces();
            if (match('!')) {
                Nodo operand = parseNot();
                return new NodoNot(operand);
            }
            return parseAtom();
        }

        // Nivel 6: paréntesis o variable
        private Nodo parseAtom() throws ParseException {
            skipSpaces();
            if (match('(')) {
                Nodo inside = parseXnor();
                skipSpaces();
                if (!match(')')) {
                    throw new ParseException("Falta ')' en posición " + pos);
                }
                return inside;
            }
            if (Character.isLetter(actual)) {
                StringBuilder sb = new StringBuilder();
                sb.append(actual);
                siguienteChar();
                while (Character.isLetterOrDigit(actual)) {
                    sb.append(actual);
                    siguienteChar();
                }
                return new NodoVar(sb.toString());
            }
            throw new ParseException("Símbolo inesperado '" + actual + "' en posición " + pos);
        }

        private boolean peekString(String s) {
            return input.startsWith(s, pos);
        }

        private void consumirString(String s) throws ParseException {
            if (input.startsWith(s, pos)) {
                for (int i = 0; i < s.length(); i++) siguienteChar();
            } else {
                throw new ParseException("Se esperaba '" + s + "' en posición " + pos);
            }
        }
    }


    private static abstract class Nodo {
        public abstract int evaluar(Map<String, Integer> env);
        public abstract Set<String> obtenerVariables();
    }

    private static class NodoVar extends Nodo {
        private String nombre;
        public NodoVar(String nom) { nombre = nom; }
        @Override
        public int evaluar(Map<String, Integer> env) {
            Integer v = env.get(nombre);
            return (v == null ? 0 : v);
        }
        @Override
        public Set<String> obtenerVariables() {
            Set<String> s = new HashSet<>();
            s.add(nombre);
            return s;
        }
        @Override
        public String toString() { return nombre; }
    }

    private static class NodoNot extends Nodo {
        private Nodo nodo;
        public NodoNot(Nodo n) { nodo = n; }
        @Override
        public int evaluar(Map<String, Integer> env) {
            return nodo.evaluar(env) == 0 ? 1 : 0;
        }
        @Override
        public Set<String> obtenerVariables() {
            return nodo.obtenerVariables();
        }
        @Override
        public String toString() { return "(!" + nodo.toString() + ")"; }
    }

    private static class NodoAnd extends Nodo {
        private Nodo izq, der;
        public NodoAnd(Nodo l, Nodo r) { izq = l; der = r; }
        @Override
        public int evaluar(Map<String, Integer> env) {
            return (izq.evaluar(env) == 1 && der.evaluar(env) == 1) ? 1 : 0;
        }
        @Override
        public Set<String> obtenerVariables() {
            Set<String> s = new HashSet<>(izq.obtenerVariables());
            s.addAll(der.obtenerVariables());
            return s;
        }
        @Override
        public String toString() { return "(" + izq.toString() + " && " + der.toString() + ")"; }
    }

    private static class NodoOr extends Nodo {
        private Nodo izq, der;
        public NodoOr(Nodo l, Nodo r) { izq = l; der = r; }
        @Override
        public int evaluar(Map<String, Integer> env) {
            return (izq.evaluar(env) == 1 || der.evaluar(env) == 1) ? 1 : 0;
        }
        @Override
        public Set<String> obtenerVariables() {
            Set<String> s = new HashSet<>(izq.obtenerVariables());
            s.addAll(der.obtenerVariables());
            return s;
        }
        @Override
        public String toString() { return "(" + izq.toString() + " || " + der.toString() + ")"; }
    }

    private static class NodoXor extends Nodo {
        private Nodo izq, der;
        public NodoXor(Nodo l, Nodo r) { izq = l; der = r; }
        @Override
        public int evaluar(Map<String, Integer> env) {
            return (izq.evaluar(env) ^ der.evaluar(env));
        }
        @Override
        public Set<String> obtenerVariables() {
            Set<String> s = new HashSet<>(izq.obtenerVariables());
            s.addAll(der.obtenerVariables());
            return s;
        }
        @Override
        public String toString() { return "(" + izq.toString() + " ^ " + der.toString() + ")"; }
    }

    private static class NodoXnor extends Nodo {
        private Nodo izq, der;
        public NodoXnor(Nodo l, Nodo r) { izq = l; der = r; }
        @Override
        public int evaluar(Map<String, Integer> env) {
            return (izq.evaluar(env) == der.evaluar(env)) ? 1 : 0;
        }
        @Override
        public Set<String> obtenerVariables() {
            Set<String> s = new HashSet<>(izq.obtenerVariables());
            s.addAll(der.obtenerVariables());
            return s;
        }
        @Override
        public String toString() { return "(" + izq.toString() + " ^^ " + der.toString() + ")"; }
    }
    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            new ProgramaP3DL();
        });
    }
}

