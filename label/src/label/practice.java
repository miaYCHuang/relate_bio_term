package label;


import java.awt.BorderLayout;
import java.awt.CardLayout;
import java.awt.Color;
import java.awt.Font;
import java.awt.GridBagConstraints;
import java.awt.GridBagLayout;
import java.awt.Image;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.BufferedReader;

import java.io.FileNotFoundException;
import java.io.FileReader;

import java.io.IOException;
import java.util.Arrays;
import java.util.Random;

import javax.swing.BorderFactory;

import javax.swing.ImageIcon;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;

import javax.swing.Timer;
import javax.swing.UIManager;

import javax.swing.UnsupportedLookAndFeelException;
import javax.swing.border.Border;
import javax.swing.border.CompoundBorder;
import javax.swing.border.EmptyBorder;

//https://blog.51cto.com/u_15127657/4192053
public class practice implements ActionListener{
	Image img;
	static JPanel panel1,JPintro,JPprac;
	static CardLayout cardLayout1,cardLayout2;
	static int j=1,nunmber=11;//�����MCSV���ؤ@��
	static JButton btn_next,btn_pre;
	static JFrame jframe;
	
	
	private static Timer tim;
	static String[] x = null, y = null;// X->pair1,y->pair2(�]�N�Oquestion1,question2)
	static int[] Random_Num = null;//���åX�D����(�H���üƥX�{question -> �ϨC�ӤHQ���Ǥ��P)
	static int rdm_index = 0;//Random_Num��index  ��eindex
	static int number = 11;/*! nunmber�����MCSV���ؤ@�� nunmber=pair�ƶq+1(title) !*/
	static int countdoown_id=0;//�˼ƭp�� �C��W�[1
	static int current_time_tmp = 0;//�Ȧs�{�b"���D"�Ҫ�O���ɶ�
	static int total_time = 0;//�`�@��O���ɶ�(���P�D)
	static int[] timeArray = new int[number]; // �s��C�@�D�ɶ�
	static boolean[] backtrack = new boolean[number]; // �T�{�O�_�^��W�@�D (�Ȧs)
	static String[] arr_ans = new String[number];//��������
	static int label_level = 10;//10�Ӽе��{��
	
	//�D���� �����card card1->page_start ,card2->demo
	static final JFrame mainPage = new JFrame();
	static JPanel main_Panel;
	static CardLayout cardLayout;
	static JLabel JL_start;//page_start����r
	
	static final JPanel demo = new JPanel(new BorderLayout());
	//�W��
	static JPanel panel_N;
	static JButton PREVIOUS_BUTTON = new JButton("�W�@�D");
	static JButton NEXT_BUTTON = new JButton("�U�@�D");
	static final JLabel title = new JLabel("", JLabel.CENTER);
	static JLabel time, time2, time_title, time_title2;
	//time->���D�Ҫ�ɶ�, time2->�{���`�@���ɶ�
	//����
	static JPanel panel_q;
	static final JLabel question1 = new JLabel("Label1", JLabel.CENTER);
	static final JLabel vs = new JLabel("VS", JLabel.CENTER);
	static final JLabel question2 = new JLabel("Label2", JLabel.CENTER);
	//�U��
	static JPanel radioPanel;
	static JButton[] buttons  = new JButton[number];

	static int time_cnt=0;//�p��ɶ�
	
	
	static int now_totoalTime_tmp=0;//������e�ɶ�  �P�_�O ��Үɶ� �٬O �����D�ت����j�ɶ�
    
	
	public static void main(String[] args) throws IOException, ClassNotFoundException, InstantiationException, IllegalAccessException, UnsupportedLookAndFeelException {
		JPintro = new JPanel();
        cardLayout1 = new CardLayout();
        JPintro.setLayout(new BorderLayout());
        //frame.setBackground(Color.decode("#F4FCD9"));
        
        jframe = new JFrame();
        jframe.setLayout(cardLayout1);
        
        cardLayout2 = new CardLayout();
        panel1 = new JPanel();        
        panel1.setLayout(cardLayout2);
        panel1.setBackground(Color.WHITE);
       
        
        JPanel p1 = new JPanel();
        JPanel p2 = new JPanel();
        JPanel p3 = new JPanel();
        JPanel p4 = new JPanel();
        JPanel p5 = new JPanel();
        JPanel p6 = new JPanel();
        
        p1.setBackground(Color.WHITE);
        p2.setBackground(Color.WHITE);
        p3.setBackground(Color.WHITE);
        p4.setBackground(Color.WHITE);
        p5.setBackground(Color.WHITE);
        p6.setBackground(Color.WHITE);
        
        JLabel label1 = new JLabel();
        JLabel label2 = new JLabel();
        JLabel label3 = new JLabel();
        JLabel label4 = new JLabel();
        JLabel label5 = new JLabel();
        //JLabel label6 = new JLabel();

        
        label1.setIcon(new ImageIcon("1-1.png"));
        label2.setIcon(new ImageIcon("2-1.png"));
        label3.setIcon(new ImageIcon("3-1.png"));
        label4.setIcon(new ImageIcon("4-1.png"));
        label5.setIcon(new ImageIcon("5-1.png"));
        
        p1.add(label1);
        p2.add(label2);
        p3.add(label3);
        p4.add(label4);
        p5.add(label5);
        //p6.add(label6);
        
        panel1.add("pic1",p1);
        panel1.add("pic2",p2);
        panel1.add("pic3",p3);
        panel1.add("pic4",p4);
        panel1.add("pic5",p5);
        //panel1.add("pic6",p5);
        
        JPanel panel2 = new JPanel();
        panel2.setBackground(Color.WHITE);
        btn_next = new JButton("�U�@�B");
        btn_pre = new JButton("�W�@�B");
        btn_next.addActionListener(new practice());  
        btn_pre.addActionListener(new practice()); 
        btn_next.setActionCommand("next_step");
        btn_pre.setActionCommand("pre_step");
        btn_pre.setVisible(false);      
        UIManager.setLookAndFeel("com.sun.java.swing.plaf.windows.WindowsClassicLookAndFeel"); //�˦�
        panel2.add(btn_pre);
        panel2.add(btn_next);

        //frame.pack();
        //cardLayout.show(panel1, "pic3");;
        
        JPintro.add(BorderLayout.CENTER,panel1);
        JPintro.add(BorderLayout.SOUTH,panel2);
        
        
        JPprac = new JPanel();
        JPprac.setBackground(Color.blue);
        
               
        jframe.add("intro",JPintro);
        jframe.add("prac",demo);
        jframe.setSize(1510, 850);
        jframe.setLocation(50,10); 
        jframe.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        jframe.setVisible(true); 
    }
	
	

	public static void label(String path,int num) throws FileNotFoundException{
		
		//num=number=pair�ƶq+1(title)
		// �üƨ��ȡA�����ơ���������������������������������������������������������������������������������������������������������������������������������������������������
		Random r = new Random();
		Random_Num = new int[num - 1];// -1(title) �H���ͦ��üƪ��}�C  ���פ֤@
		
		int[] Check_Num = new int[num - 1];

		for (int id1 = 0; id1 < Random_Num.length; id1++) {
			Random_Num[id1] = r.nextInt(num - 1) + 1; // �H������1~(num - 1)�ӼƦr��J Random_Num[]
			for (int id2 = 0; id2 < id1;) { // �P�e�ƦC����A�Y���ۦP�h�A���ü�
				if (Random_Num[id2] == Random_Num[id1]) {
					Random_Num[id1] = r.nextInt(num - 1) + 1;
					id2 = 0; // �׭����s�üƫ�S���ͬۦP�Ʀr�A�Y�X�{���СA�j��q�Y�}�l���s����Ҧ���
				} else {
					id2++; // �Y�������ƫh�U�@�Ӽ�
				}
			}

		}

		//�ˬd���L�ʭ�
		System.out.print("Not sort(random): ");
		for (int id1 = 0; id1 < Random_Num.length; id1++) {
			Check_Num[id1] = Random_Num[id1];
			System.out.print(Random_Num[id1] + " ");//�H���ü�
		}
		Arrays.sort(Check_Num);// �Ƨ�
		System.out.println();
		System.out.print("sort: ");
		for (int id1 = 0; id1 < Check_Num.length; id1++)
			System.out.print(Check_Num[id1] + " ");//�H���üƱƧǫ�
		System.out.println();
		// �üƨ��ȡA�����ơ���������������������������������������������������������������������������������������������������������������������������������������������������
		
		



		// Ū�ɡ���������������������������������������������������������������������������������������������������������������������������������������������������
		String line = "";
		final String delimiter = ",";
		try {
			String filePath = path;
			FileReader fileReader = new FileReader(filePath);
			BufferedReader reader = new BufferedReader(fileReader);
			x = new String[num];
			y = new String[num];

			int ids = 0;
			// X��Y�W�L�|�Ӧr�N����
			while ((line = reader.readLine()) != null) // loops through every line until null found
			{
				String[] token = line.split(delimiter); // separate every token by comma
			
				int space_cnt = 0;
				String str_x = "";

				for (int j = 0; j < token[0].length(); j++) {//question1
					if (token[0].charAt(j) == 32) {
						space_cnt++;
						if (space_cnt % 4 == 0) {
							str_x += "<br>";

						} else {
							str_x += token[0].charAt(j);
						}
					} else {
						str_x += token[0].charAt(j);
					}
				}

				int space_cnt2 = 0;
				String str_y = "";
				for (int j = 0; j < token[1].length(); j++) {//question2
					if (token[1].charAt(j) == 32) {
						space_cnt2++;
						if (space_cnt2 % 4 == 0) {
							str_y += "<br>";

						} else {
							str_y += token[1].charAt(j);
						}
					} else {
						str_y += token[1].charAt(j);
					}
				}
				x[ids] = str_x;//�W�[�������s�J�}�C
				y[ids] = str_y;
				ids++;
			}
			reader.close();

		} catch (IOException e) {
			e.printStackTrace();
		}
		// Ū�ɡ���������������������������������������������������������������������������������������������������������������������������������������������������





		// �����ɼg�Ĥ@row(���D��r)
		/*try {
			File csv = new File("answer.csv");// CSV�ɮ�
			BufferedWriter bw = new BufferedWriter(new FileWriter(csv, true));
			// �s�W�@����
			// bw.newLine();
			bw.write("id" + "," + "num" + "," + "ans" + "," + "time" + "," + "backtrack");
			bw.close();
		} catch (FileNotFoundException e) {
			// ����File����ͦ��ɪ����`
			e.printStackTrace();
		} catch (IOException e) {
			// ����BufferedWriter���������ɪ����`
			e.printStackTrace();
		}*/


		
		demo.setBackground(Color.decode("#F3F0D7"));



		// TOP����������������������������������������������������������������������������������������������������������������������������������������������������
		Font fntSize50 = new Font("Serief", Font.BOLD, 50);
		Font fntSize30 = new Font("Serief", Font.BOLD, 30);
		title.setFont(fntSize30);
		title.setText(
				"<html>Question: <font color=\"red\">" + (rdm_index + 1) + "</font> / " + (number - 1) + "</html>");
				//(�ثe�D��)+1->index=0���Ĥ@�D,   (�����D��)-1�]��title(index[0])����
		title.setBorder(new EmptyBorder(0, 0, 0, 0));// top,left,bottom,right

		time = new JLabel("", JLabel.CENTER);
		time2 = new JLabel("", JLabel.CENTER);
		time_title = new JLabel("", JLabel.CENTER);
		time_title2 = new JLabel("", JLabel.CENTER);

		time_title.setText(" Current time:");
		time_title2.setText(" / Total time:");

		time.setForeground(Color.red);

		time.setFont(fntSize30);
		time2.setFont(fntSize30);
		time_title.setFont(fntSize30);
		time_title2.setFont(fntSize30);

		time.setBorder(new EmptyBorder(10, 0, 0, 0));// top,left,bottom,right
		time2.setBorder(new EmptyBorder(10, 0, 0, 0));
		time_title.setBorder(new EmptyBorder(10, 0, 0, 0));
		time_title2.setBorder(new EmptyBorder(10, 0, 0, 0));

		PREVIOUS_BUTTON.setBackground(Color.decode("#cfe2f3"));		
		NEXT_BUTTON.setBackground(Color.decode("#cfe2f3"));
		
		panel_N = new JPanel();

		panel_N.setBackground(Color.decode("#96CEB4"));// ���D

		panel_N.add(PREVIOUS_BUTTON);
		panel_N.add(title);
		panel_N.add(NEXT_BUTTON);
		panel_N.add(time_title);
		panel_N.add(time);
		panel_N.add(time_title2);
		panel_N.add(time2);
		

		if (rdm_index == 0) {
			PREVIOUS_BUTTON.setVisible(false);
			NEXT_BUTTON.setVisible(false);
		}

		previousBtn();
		nextBtn();

		//tim.setActionCommand("time");
		// TOP����������������������������������������������������������������������������������������������������������������������������������������������������





		// CENTER����������������������������������������������������������������������������������������������������������������������������������������������������
		panel_q = new JPanel();
		panel_q.setLayout(new GridBagLayout());
		GridBagConstraints gbc = new GridBagConstraints();

		question1.setText("<html><body><center>" + x[Random_Num[rdm_index]] + "<center><body></html>");
		question2.setText("<html><body><center>" + y[Random_Num[rdm_index]] + "<center><body></html>");
		Border blackline = BorderFactory.createLineBorder(Color.black);
		Border margin = new EmptyBorder(30, 30, 35, 30);// �W���U�k
		question1.setBorder(new CompoundBorder(blackline, margin));
		question2.setBorder(new CompoundBorder(blackline, margin));

		question1.setFont(fntSize50);
		vs.setFont(fntSize50);
		question2.setFont(fntSize50);

		panel_q.setBackground(Color.decode("#F3F0D7"));// ���D�O

		gbc.weightx = 1;

		gbc.gridx = 0;
		gbc.gridy = 0;
		panel_q.add(question1, gbc);
		gbc.gridx = 0;
		gbc.gridy = 1;
		panel_q.add(vs, gbc);
		gbc.gridx = 0;
		gbc.gridy = 2;
		panel_q.add(question2, gbc);
		// CENTER����������������������������������������������������������������������������������������������������������������������������������������������������



		// Bottom����������������������������������������������������������������������������������������������������������������������������������������������������
		countdown1();
		demo.add(BorderLayout.CENTER, panel_q);
		demo.add(BorderLayout.NORTH, panel_N);
		// Bottom����������������������������������������������������������������������������������������������������������������������������������������������������
		
		//�]�wTimer�w�ɾ�,�ñҰ�
        tim = new Timer(1000,new practice());
        tim.setActionCommand("time");
        tim.start();
      //����������������������������������������������������������������������������������������������������������������������������������������������������
	    }
	
	public static void countdown1() {
		
		Font btn = new Font("Serief", Font.BOLD, 50);
		for(int i = 0; i < label_level; i++){
			buttons[i] = new JButton(String.valueOf(i+1)); //i=0 -> 1
			buttons[i].setActionCommand(String.valueOf(i+1)); 
			buttons[i].setBackground(Color.decode("#cfe2f3"));
			buttons[i].setBorderPainted(false);
			buttons[i].setForeground(Color.decode("#3d85c6"));
			buttons[i].setFont(btn);
			buttons[i].addActionListener(new practice());

		}

		radioPanel = new JPanel(new GridBagLayout());// int rows, int cols
		radioPanel.setBackground(Color.decode("#96CEB4"));
		
		JLabel degree = new JLabel("Degree of Relatedness");
		JLabel high = new JLabel("High");
		JLabel low = new JLabel("Low");
		JLabel space = new JLabel("   ");
		
		GridBagConstraints gbc_r = new GridBagConstraints();
		GridBagConstraints gbc_d = new GridBagConstraints();

		gbc_d.gridx = 3;
		gbc_d.gridy = 0;
		gbc_d.gridwidth = 4;
		radioPanel.add(degree, gbc_d);

		gbc_r.gridx = 9;
		gbc_r.gridy = 1;
		radioPanel.add(high, gbc_r);

		gbc_r.gridx = 0;
		gbc_r.gridy = 1;
		radioPanel.add(low, gbc_r);

		Font fntSize25 = new Font("Serief", Font.BOLD, 25);
		Font fntSize20 = new Font("Serief", Font.BOLD, 20);
		high.setFont(fntSize20);
		low.setFont(fntSize20);
		degree.setFont(fntSize25);

		gbc_r.weightx = 0.5;
		gbc_r.gridx = 0;
		gbc_r.gridy = 2;
		radioPanel.add(buttons[0], gbc_r);
		gbc_r.gridx = 1;
		gbc_r.gridy = 2;
		radioPanel.add(buttons[1], gbc_r);
		gbc_r.gridx = 2;
		gbc_r.gridy = 2;
		radioPanel.add(buttons[2], gbc_r);
		gbc_r.gridx = 3;
		gbc_r.gridy = 2;
		radioPanel.add(buttons[3], gbc_r);
		gbc_r.gridx = 4;
		gbc_r.gridy = 2;
		radioPanel.add(buttons[4], gbc_r);
		gbc_r.gridx = 5;
		gbc_r.gridy = 2;
		radioPanel.add(buttons[5], gbc_r);
		gbc_r.gridx = 6;
		gbc_r.gridy = 2;
		radioPanel.add(buttons[6], gbc_r);
		gbc_r.gridx = 7;
		gbc_r.gridy = 2;
		radioPanel.add(buttons[7], gbc_r);
		gbc_r.gridx = 8;
		gbc_r.gridy = 2;
		radioPanel.add(buttons[8], gbc_r);
		gbc_r.gridx = 9;
		gbc_r.gridy = 2;
		radioPanel.add(buttons[9], gbc_r);

		gbc_r.gridy = 3;
		radioPanel.add(space, gbc_r); // �h�@�C�����s���n�K���U��

		demo.add(BorderLayout.SOUTH, radioPanel);
        
    }
	
	
	@Override
	public void actionPerformed(ActionEvent e) {
		// TODO Auto-generated method stub
		//JButton b =(JButton)e.getSource();
		String cmd = e.getActionCommand();
		//System.out.print(b);
		
		if(cmd == "next_step" ) {
			j++;
			if(j==2) {
				btn_pre.setVisible(true);
			}else if(j==5) {
				btn_next.setText("�}�l�m��");
			}else if(j==6){
				try {
		    		
					label("pair10.csv",nunmber);
					jframe.setSize(1500, 800);
					jframe.setLocation(50,10);
				} catch (FileNotFoundException e1) {
					// TODO Auto-generated catch block
					e1.printStackTrace();
					
				}
				cardLayout1.show(jframe.getContentPane(), "prac");
			}
			System.out.println("BTN"+"  i="+j);			
			cardLayout2.show(panel1, "pic"+j);			
		}else if(cmd == "pre_step") {
			j--;
			if(j<=1)j=1;
			else if (j<=5 || j>=1) btn_next.setText("�U�@�B");
			
			System.out.println("BTN"+"  i="+j);			
			cardLayout2.show(panel1, "pic"+j);
			
		}else if (cmd == "time") {//demo��l�p��  �C�����@��
			time_cnt++;
			total_time++; // �`�ɶ�
			time.setText(String.valueOf(time_cnt));
			time2.setText(String.valueOf(total_time));
			
			
			
			if(backtrack[rdm_index] == true){//���I��W�U�D
				if (Integer.parseInt(time2.getText()) > now_totoalTime_tmp+5){//���j5��H�W������Ҹ��D(���ק藍�A�p�ɶ��A�ק�h�|�[�W��Үɶ�)
					timeArray[rdm_index]=time_cnt;
					System.out.println("���");
					System.out.println("���");
				}
				//5��H�U�������D�ت����j�ɶ�  ���p���
		
			}

			
			
			
			/* �^�����D������קK���H�ë� */
			panel_N.setVisible(true);
			panel_q.setVisible(true);
			radioPanel.setVisible(true);
			/* �^�����D������קK���H�ë� */
			
			
		}

		
		
		else if (cmd == "time_start") {//�˼Ƥ���
			countdoown_id++;
			JL_start.setText("<html><body><center>�˼ƫ�i�J<br>" + String.valueOf((5 - countdoown_id)) + "<center><body></html>");
			if (countdoown_id == 5) {
				
				countdoown_id = 0;
				tim.setActionCommand("time");
				try {
					label("test100.csv", number);
				} catch (FileNotFoundException e1) {
					e1.printStackTrace();
				}
				cardLayout.show(main_Panel, "dmo");//�ഫ��dmo����
				panel_N.setVisible(false);
				panel_q.setVisible(false);
				radioPanel.setVisible(false);
		}








		} else if (cmd == "next") {//�U�@�D���s
			now_totoalTime_tmp=Integer.parseInt(time2.getText());
			System.out.println(now_totoalTime_tmp);
			
			backtrack[rdm_index] = true;
			rdm_index++;
			
			title.setText("<html>Question: <font color=\"red\">" + (rdm_index + 1) + "</font> / " + (number - 1) + "</html>");
			question1.setText("<html><body><center>" + x[Random_Num[rdm_index]] + "<center><body></html>");
			question2.setText("<html><body><center>" + y[Random_Num[rdm_index]] + "<center><body></html>");

			if (arr_ans[rdm_index] != null){//�����L���D��				
				PREVIOUS_BUTTON.setVisible(true);				
				for(int i = 0; i < label_level; i++) {//��ܵ���
					if (i== Integer.parseInt(arr_ans[rdm_index])-1){//-1 -> button�q0�}�l
						
						buttons[i].setBackground(Color.decode("#3d85c6"));
						buttons[i].setForeground(Color.decode("#cfe2f3"));
					}else{
						buttons[i].setBackground(Color.decode("#cfe2f3"));
						buttons[i].setForeground(Color.decode("#3d85c6"));
					}
				}
				time_cnt=timeArray[rdm_index];//�q���e�������ɶ��}�l�p��
				
			}else{//�S���L
				time_cnt=0;//���F�L�ɶ��k�s
				backtrack[rdm_index] = false;
				NEXT_BUTTON.setVisible(false);
				for(int i = 0; i < label_level; i++){
					buttons[i].setBackground(Color.decode("#cfe2f3"));
					buttons[i].setForeground(Color.decode("#3d85c6"));
				}
									
			}
			
			System.out.println("�U�@�Drdm_index: "+rdm_index+" ans: "+arr_ans[rdm_index]+" time:"+timeArray[rdm_index]+" back:"+backtrack[rdm_index]);
			
			/* �^�����D������קK���H�ë� */
			panel_N.setVisible(false);
			panel_q.setVisible(false);
			radioPanel.setVisible(false);
			/* �^�����D������קK���H�ë� */
			
		
			
			
		} else if (cmd == "previous") {//�W�@�D���s
		
			
			now_totoalTime_tmp=Integer.parseInt(time2.getText());
			System.out.println(now_totoalTime_tmp);
			
			
			rdm_index--;			
			NEXT_BUTTON.setVisible(true);
			backtrack[rdm_index] = true;
			if (rdm_index == 0) {//�Ĥ@�� ����
				PREVIOUS_BUTTON.setVisible(false);
			}
			
			
		
			title.setText("<html>Question: <font color=\"red\">" + (rdm_index + 1) + "</font> / " + (number - 1) + "</html>");			
			question1.setText("<html><body><center>" + x[Random_Num[rdm_index]] + "<center><body></html>");
			question2.setText("<html><body><center>" + y[Random_Num[rdm_index]] + "<center><body></html>");
			
			for(int i = 0; i < label_level; i++) {//��ܵ���
				if (i== Integer.parseInt(arr_ans[rdm_index])-1){//-1 -> button�q0�}�l
					buttons[i].setBackground(Color.decode("#3d85c6"));
					buttons[i].setForeground(Color.decode("#cfe2f3"));
				}else{
					buttons[i].setBackground(Color.decode("#cfe2f3"));
					buttons[i].setForeground(Color.decode("#3d85c6"));
				}
			}
			
			System.out.println("�U�@�Drdm_index: "+rdm_index+" ans: "+arr_ans[rdm_index]+" time:"+timeArray[rdm_index]+" back:"+backtrack[rdm_index]);
			
			time_cnt=timeArray[rdm_index];//�q���e�������ɶ��}�l�p��
			
			/* �^�����D������קK���H�ë� */
			panel_N.setVisible(false);
			panel_q.setVisible(false);
			radioPanel.setVisible(false);
			/* �^�����D������קK���H�ë� */
			

			
			
			
			
		} else if (cmd.equals("1") || cmd.equals("2") || cmd.equals("3") || cmd.equals("4") || cmd.equals("5") || cmd.equals("6") || cmd.equals("7") || cmd.equals("8") || cmd.equals("9") || cmd.equals("10") ) {
			System.out.println("btn");
			if(arr_ans[rdm_index]==null || arr_ans[rdm_index] != cmd){//�S�����L �� �קﵪ��
		
				arr_ans[rdm_index] = cmd;
				timeArray[rdm_index] = time_cnt;
				
				/*try {// ���s���U��O�����										
					File csv = new File("answer.csv");// CSV�ɮ�
					BufferedWriter bw = new BufferedWriter(new FileWriter(csv, true));
					// �s�W�@����
					bw.newLine();
					bw.write(Random_Num[rdm_index] + "," + (rdm_index + 1) + "," + cmd + "," + time.getText() + ","
							+ backtrack[rdm_index]);
					if (rdm_index == number - 2) bw.newLine();// �s����檺�ܤ���
					bw.close();
				} catch (FileNotFoundException e1) {
					// ����File����ͦ��ɪ����`
					e1.printStackTrace();
				} catch (IOException e1) {
					// ����BufferedWriter���������ɪ����`
					e1.printStackTrace();
				}*/

			}//�P�˵��� ������
			
			
			
			/* �^�����D������קK���H�ë� */
			panel_N.setVisible(false);
			panel_q.setVisible(false);
			radioPanel.setVisible(false);
			/* �^�����D������קK���H�ë� */
			
			//!!!!!!!!!!!!!!!!!!!
			rdm_index++;// �U�@�Did++
			//!!!!!!!!!!!!!!!!!!!
			PREVIOUS_BUTTON.setVisible(true);
			title.setText("<html>Question: <font color=\"red\">" + (rdm_index + 1) + "</font> / " + (number - 1) + "</html>");
					
					
			//����
			if (rdm_index > number - 2) {// �W�L��ƼƴN����  rdm_index����=9 number=11(�Hpair 10�� + 1(���D) ����)
				tim.stop();	
				System.out.println("�`�@��O:"+time2.getText());
				panel_N.setVisible(true);
				time.setVisible(false);
				time2.setVisible(false);
				time_title.setVisible(false);
				time_title2.setVisible(false);
				PREVIOUS_BUTTON.setVisible(false);
				NEXT_BUTTON.setVisible(false);
				title.setText("����");				
				panel_q.setVisible(true);				
				vs.setText("<html><body><center><p>�Чi�������H��</p><br><p>�P�¦X�@</p><br><center><body></html>");
				question1.setVisible(false);
				question2.setVisible(false);

				
			//�U�@��
			} else {// �S�W�L�A��ܤU�@���A�ɶ����p
			
				
				
				/*���ܫ��s�C��*/
				if (arr_ans[rdm_index] != null){//�����L���D��
					now_totoalTime_tmp=Integer.parseInt(time2.getText());
					time_cnt=timeArray[rdm_index];
					for(int i = 0; i < label_level; i++) {
						if (i== Integer.parseInt(arr_ans[rdm_index])-1){//-1 -> button�q0�}�l
							buttons[i].setBackground(Color.decode("#3d85c6"));
							buttons[i].setForeground(Color.decode("#cfe2f3"));
						}else{
							buttons[i].setBackground(Color.decode("#cfe2f3"));
							buttons[i].setForeground(Color.decode("#3d85c6"));
						}
					}
				}else{//�S���L
					time_cnt=0;
					backtrack[rdm_index] = false;
					NEXT_BUTTON.setVisible(false);
					for(int i = 0; i < label_level; i++) {
						buttons[i].setBackground(Color.decode("#cfe2f3"));	
						buttons[i].setForeground(Color.decode("#3d85c6"));
					}				
				}
				/*���ܫ��s�C��*/
				

				if (rdm_index == Random_Num.length - 1) {//�̫�@��
					NEXT_BUTTON.setVisible(false);
				}
			
				//tim.setActionCommand("time");
				question1.setText("<html><body><center>" + x[Random_Num[rdm_index]] + "<center><body></html>");
				question2.setText("<html><body><center>" + y[Random_Num[rdm_index]] + "<center><body></html>");
				
				
			}
			

			

		}

		
	}
	
	public static void previousBtn() {
		PREVIOUS_BUTTON.setActionCommand("previous");
		PREVIOUS_BUTTON.addActionListener(new practice());
	}

	public static void nextBtn() {
		NEXT_BUTTON.setActionCommand("next");
		NEXT_BUTTON.addActionListener(new practice());
	}
	
	
}