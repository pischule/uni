package by.bsu.tp;

import by.bsu.tp.config.Config;
import by.bsu.tp.gui.AppPanel;

import javax.swing.*;

public class App {

    public static void main(String[] args) {
        SwingUtilities.invokeLater(App::createAndShowGUI);
    }

    private static void createAndShowGUI() {
        try {
            UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName());
        } catch (IllegalAccessException | InstantiationException | UnsupportedLookAndFeelException | ClassNotFoundException e) {
            e.printStackTrace();
        }

        JFrame f = new JFrame(Config.APP_NAME);
        f.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        f.setSize(Config.WINDOW_SIZE);
        f.add(new AppPanel());
        f.setVisible(true);
    }

}

