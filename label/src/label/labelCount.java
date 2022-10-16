package label;

import java.awt.*;
import java.io.*;
import java.util.Arrays;
import java.util.Random;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import javax.swing.*;
import javax.swing.border.Border;
import javax.swing.border.CompoundBorder;
import javax.swing.border.EmptyBorder;

/*
 * 物件
 * http://cc.cust.edu.tw/~ccchen/doc/ch17.pdf
 * 版面位置
 * http://yhhuang1966.blogspot.com/2014/02/java-swing-jbutton-jlabel-jtextfield.html
 * 讀黨
 * https://www.delftstack.com/zh-tw/howto/java/parse-csv-in-java/
 * 檔案位置
 * https://stackoverflow.com/questions/13592325/exception-in-thread-main-java-io-filenotfoundexception-error
 * 寫入
 * https://www.itread01.com/content/1546815604.html
 * 點擊取位置
 * https://www.796t.com/post/YW9ja2U=.html
 * 計時
 * https://www.itread01.com/p/300596.html
 * 亂數取不重複
 * https://gist.github.com/HabaCo/140a3ad71ee0bf15b0f4
 */

class labelCount implements ActionListener {
	//默認JPanel->FlowLayout  JFrame->BorderLayout
	
	//初始
	private static Timer tim;
	static String[] x = null, y = null;// X->pair1,y->pair2(也就是question1,question2)
	static int[] Random_Num = null;//打亂出題順序(隨機亂數出現question -> 使每個人Q順序不同)
	static int rdm_index = 0;//Random_Num的index  當前index
	static int number = 101;/*! nunmber必須和CSV項目一樣 nunmber=pair數量+1(title) !*/
	static int countdoown_id=0;//倒數計時 每秒增加1
	static int current_time_tmp = 0;//暫存現在"該題"所花費之時間
	static int total_time = 0;//總共花費的時間(不同題)
	static int[] timeArray = new int[number]; // 存放每一題時間
	static boolean[] backtrack = new boolean[number]; // 確認是否回到上一題 (暫存)
	static String[] arr_ans = new String[number];//紀錄答案
	static int label_level = 10;//10個標註程度
	
	//主頁面 有兩個card card1->page_start ,card2->demo
	static final JFrame mainPage = new JFrame();
	static JPanel main_Panel;
	static CardLayout cardLayout;
	static JLabel JL_start;//page_start的文字
	
	static final JPanel demo = new JPanel(new BorderLayout());
	//上方
	static JPanel panel_N;
	static JButton PREVIOUS_BUTTON = new JButton("上一題");
	static JButton NEXT_BUTTON = new JButton("下一題");
	static final JLabel title = new JLabel("", JLabel.CENTER);
	static JLabel time, time2, time_title, time_title2;
	//time->該題所花時間, time2->程式總共的時間
	//中間
	static JPanel panel_q;
	static final JLabel question1 = new JLabel("Label1", JLabel.CENTER);
	static final JLabel vs = new JLabel("VS", JLabel.CENTER);
	static final JLabel question2 = new JLabel("Label2", JLabel.CENTER);
	//下方
	static JPanel radioPanel;
	static JButton[] buttons  = new JButton[number];

	static int time_cnt=0;//計算時間
	
	
	static int now_totoalTime_tmp=0;//紀錄當前時間  判斷是 思考時間 還是 切換題目的間隔時間
	
	public static void label(String path, int num) throws FileNotFoundException {
		
		//num=number=pair數量+1(title)
		// 亂數取值，不重複↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
		Random r = new Random();
		Random_Num = new int[num - 1];// -1(title) 隨機生成亂數的陣列  長度少一
		
		int[] Check_Num = new int[num - 1];

		for (int id1 = 0; id1 < Random_Num.length; id1++) {
			Random_Num[id1] = r.nextInt(num - 1) + 1; // 隨機產生1~(num - 1)個數字放入 Random_Num[]
			for (int id2 = 0; id2 < id1;) { // 與前數列比較，若有相同則再取亂數
				if (Random_Num[id2] == Random_Num[id1]) {
					Random_Num[id1] = r.nextInt(num - 1) + 1;
					id2 = 0; // 避面重新亂數後又產生相同數字，若出現重覆，迴圈從頭開始重新比較所有數
				} else {
					id2++; // 若都不重複則下一個數
				}
			}

		}

		//檢查有無缺值
		System.out.print("Not sort(random): ");
		for (int id1 = 0; id1 < Random_Num.length; id1++) {
			Check_Num[id1] = Random_Num[id1];
			System.out.print(Random_Num[id1] + " ");//隨機亂數
		}
		Arrays.sort(Check_Num);// 排序
		System.out.println();
		System.out.print("sort: ");
		for (int id1 = 0; id1 < Check_Num.length; id1++)
			System.out.print(Check_Num[id1] + " ");//隨機亂數排序後
		System.out.println();
		// 亂數取值，不重複↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑
		
		



		// 讀檔↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
		String line = "";
		final String delimiter = ",";
		try {
			String filePath = path;
			FileReader fileReader = new FileReader(filePath);
			BufferedReader reader = new BufferedReader(fileReader);
			x = new String[num];
			y = new String[num];

			int ids = 0;
			// X跟Y超過四個字就換行
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
				x[ids] = str_x;//增加完換行後存入陣列
				y[ids] = str_y;
				ids++;
			}
			reader.close();

		} catch (IOException e) {
			e.printStackTrace();
		}
		// 讀檔↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑





		// 答案檔寫第一row(標題文字)
		try {
			File csv = new File("answer.csv");// CSV檔案
			BufferedWriter bw = new BufferedWriter(new FileWriter(csv, true));
			// 新增一行資料
			// bw.newLine();
			bw.write("id" + "," + "num" + "," + "ans" + "," + "time" + "," + "backtrack");
			bw.close();
		} catch (FileNotFoundException e) {
			// 捕獲File物件生成時的異常
			e.printStackTrace();
		} catch (IOException e) {
			// 捕獲BufferedWriter物件關閉時的異常
			e.printStackTrace();
		}


		
		demo.setBackground(Color.decode("#F3F0D7"));



		// TOP↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
		Font fntSize50 = new Font("Serief", Font.BOLD, 50);
		Font fntSize30 = new Font("Serief", Font.BOLD, 30);
		title.setFont(fntSize30);
		title.setText(
				"<html>Question: <font color=\"red\">" + (rdm_index + 1) + "</font> / " + (number - 1) + "</html>");
				//(目前題目)+1->index=0為第一題,   (全部題目)-1因為title(index[0])不算
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

		panel_N.setBackground(Color.decode("#96CEB4"));// 標題

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

		tim.setActionCommand("time");
		// TOP↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑





		// CENTER↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
		panel_q = new JPanel();
		panel_q.setLayout(new GridBagLayout());
		GridBagConstraints gbc = new GridBagConstraints();

		question1.setText("<html><body><center>" + x[Random_Num[rdm_index]] + "<center><body></html>");
		question2.setText("<html><body><center>" + y[Random_Num[rdm_index]] + "<center><body></html>");
		Border blackline = BorderFactory.createLineBorder(Color.black);
		Border margin = new EmptyBorder(30, 30, 35, 30);// 上左下右
		question1.setBorder(new CompoundBorder(blackline, margin));
		question2.setBorder(new CompoundBorder(blackline, margin));

		question1.setFont(fntSize50);
		vs.setFont(fntSize50);
		question2.setFont(fntSize50);

		panel_q.setBackground(Color.decode("#F3F0D7"));// 問題板

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
		// CENTER↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑



		// Bottom↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
		RadioBtn();
		demo.add(BorderLayout.CENTER, panel_q);
		demo.add(BorderLayout.NORTH, panel_N);
		// Bottom↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑
	}
	
	
	public static void previousBtn() {
		PREVIOUS_BUTTON.setActionCommand("previous");
		PREVIOUS_BUTTON.addActionListener(new labelCount());
	}

	public static void nextBtn() {
		NEXT_BUTTON.setActionCommand("next");
		NEXT_BUTTON.addActionListener(new labelCount());
	}
	
	public static void RadioBtn() {

		Font btn = new Font("Serief", Font.BOLD, 50);
		for(int i = 0; i < label_level; i++){
			buttons[i] = new JButton(String.valueOf(i+1)); //i=0 -> 1
			buttons[i].setActionCommand(String.valueOf(i+1)); 
			buttons[i].setBackground(Color.decode("#cfe2f3"));
			buttons[i].setBorderPainted(false);
			buttons[i].setForeground(Color.decode("#3d85c6"));
			buttons[i].setFont(btn);
			buttons[i].addActionListener(new labelCount());

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
		radioPanel.add(space, gbc_r); // 多一列讓按鈕不要貼齊下面

		demo.add(BorderLayout.SOUTH, radioPanel);

	}
	
	
	
	
	
	
	

	public void actionPerformed(ActionEvent e) {
		String cmd = e.getActionCommand();
		
		if (cmd == "time") {//demo初始計時  每秒執行一次
			time_cnt++;
			total_time++; // 總時間
			time.setText(String.valueOf(time_cnt));
			time2.setText(String.valueOf(total_time));
			
			
			
			if(backtrack[rdm_index] == true){//有點選上下題
				if (Integer.parseInt(time2.getText()) > now_totoalTime_tmp+5){//間隔5秒以上為有思考該題(未修改不再計時間，修改則會加上思考時間)
					timeArray[rdm_index]=time_cnt;
					System.out.println("思考");
					System.out.println("思考");
				}
				//5秒以下為切換題目的間隔時間  不計秒數
		
			}

			
			
			
			/* 回答問題後消失避免有人亂按 */
			panel_N.setVisible(true);
			panel_q.setVisible(true);
			radioPanel.setVisible(true);
			/* 回答問題後消失避免有人亂按 */
			
			
		}

		
		
		else if (cmd == "time_start") {//倒數五秒
			countdoown_id++;
			JL_start.setText("<html><body><center>倒數後進入<br>" + String.valueOf((5 - countdoown_id)) + "<center><body></html>");
			if (countdoown_id == 5) {
				
				countdoown_id = 0;
				tim.setActionCommand("time");
				try {
					label("pair100.csv", number);
				} catch (FileNotFoundException e1) {
					e1.printStackTrace();
				}
				cardLayout.show(main_Panel, "dmo");//轉換成dmo頁面
				panel_N.setVisible(false);
				panel_q.setVisible(false);
				radioPanel.setVisible(false);
		}








		} else if (cmd == "next") {//下一題按鈕
			now_totoalTime_tmp=Integer.parseInt(time2.getText());
			System.out.println(now_totoalTime_tmp);
			
			backtrack[rdm_index] = true;
			rdm_index++;
			
			title.setText("<html>Question: <font color=\"red\">" + (rdm_index + 1) + "</font> / " + (number - 1) + "</html>");
			question1.setText("<html><body><center>" + x[Random_Num[rdm_index]] + "<center><body></html>");
			question2.setText("<html><body><center>" + y[Random_Num[rdm_index]] + "<center><body></html>");

			if (arr_ans[rdm_index] != null){//有答過的題目				
				PREVIOUS_BUTTON.setVisible(true);				
				for(int i = 0; i < label_level; i++) {//顯示答案
					if (i== Integer.parseInt(arr_ans[rdm_index])-1){//-1 -> button從0開始
						
						buttons[i].setBackground(Color.decode("#3d85c6"));
						buttons[i].setForeground(Color.decode("#cfe2f3"));
					}else{
						buttons[i].setBackground(Color.decode("#cfe2f3"));
						buttons[i].setForeground(Color.decode("#3d85c6"));
					}
				}
				time_cnt=timeArray[rdm_index];//從之前紀錄之時間開始計時
				
			}else{//沒答過
				time_cnt=0;//未達過時間歸零
				backtrack[rdm_index] = false;
				NEXT_BUTTON.setVisible(false);
				for(int i = 0; i < label_level; i++){
					buttons[i].setBackground(Color.decode("#cfe2f3"));
					buttons[i].setForeground(Color.decode("#3d85c6"));
				}
									
			}
			
			System.out.println("下一題rdm_index: "+rdm_index+" ans: "+arr_ans[rdm_index]+" time:"+timeArray[rdm_index]+" back:"+backtrack[rdm_index]);
			
			/* 回答問題後消失避免有人亂按 */
			panel_N.setVisible(false);
			panel_q.setVisible(false);
			radioPanel.setVisible(false);
			/* 回答問題後消失避免有人亂按 */
			
		
			
			
		} else if (cmd == "previous") {//上一題按鈕
		
			
			now_totoalTime_tmp=Integer.parseInt(time2.getText());
			System.out.println(now_totoalTime_tmp);
			
			
			rdm_index--;			
			NEXT_BUTTON.setVisible(true);
			backtrack[rdm_index] = true;
			if (rdm_index == 0) {//第一筆 隱藏
				PREVIOUS_BUTTON.setVisible(false);
			}
			
			
		
			title.setText("<html>Question: <font color=\"red\">" + (rdm_index + 1) + "</font> / " + (number - 1) + "</html>");			
			question1.setText("<html><body><center>" + x[Random_Num[rdm_index]] + "<center><body></html>");
			question2.setText("<html><body><center>" + y[Random_Num[rdm_index]] + "<center><body></html>");
			
			for(int i = 0; i < label_level; i++) {//顯示答案
				if (i== Integer.parseInt(arr_ans[rdm_index])-1){//-1 -> button從0開始
					buttons[i].setBackground(Color.decode("#3d85c6"));
					buttons[i].setForeground(Color.decode("#cfe2f3"));
				}else{
					buttons[i].setBackground(Color.decode("#cfe2f3"));
					buttons[i].setForeground(Color.decode("#3d85c6"));
				}
			}
			
			System.out.println("下一題rdm_index: "+rdm_index+" ans: "+arr_ans[rdm_index]+" time:"+timeArray[rdm_index]+" back:"+backtrack[rdm_index]);
			
			time_cnt=timeArray[rdm_index];//從之前紀錄之時間開始計時
			
			/* 回答問題後消失避免有人亂按 */
			panel_N.setVisible(false);
			panel_q.setVisible(false);
			radioPanel.setVisible(false);
			/* 回答問題後消失避免有人亂按 */
			

			
			
			
			
		} else if (cmd.equals("1") || cmd.equals("2") || cmd.equals("3") || cmd.equals("4") || cmd.equals("5") || cmd.equals("6") || cmd.equals("7") || cmd.equals("8") || cmd.equals("9") || cmd.equals("10") ) {
			
			if(arr_ans[rdm_index]==null || arr_ans[rdm_index] != cmd){//沒紀錄過 或 修改答案
		
				arr_ans[rdm_index] = cmd;
				timeArray[rdm_index] = time_cnt;
				
				try {// 按鈕按下後記錄資料										
					File csv = new File("answer.csv");// CSV檔案
					BufferedWriter bw = new BufferedWriter(new FileWriter(csv, true));
					// 新增一行資料
					bw.newLine();
					bw.write(Random_Num[rdm_index] + "," + (rdm_index + 1) + "," + cmd + "," + time.getText() + ","
							+ backtrack[rdm_index]);
					if (rdm_index == number - 2) bw.newLine();// 連續執行的話分行
					bw.close();
				} catch (FileNotFoundException e1) {
					// 捕獲File物件生成時的異常
					e1.printStackTrace();
				} catch (IOException e1) {
					// 捕獲BufferedWriter物件關閉時的異常
					e1.printStackTrace();
				}

			}//同樣答案 不紀錄
			
			
			
			/* 回答問題後消失避免有人亂按 */
			panel_N.setVisible(false);
			panel_q.setVisible(false);
			radioPanel.setVisible(false);
			/* 回答問題後消失避免有人亂按 */
			
			//!!!!!!!!!!!!!!!!!!!
			rdm_index++;// 下一題id++
			//!!!!!!!!!!!!!!!!!!!
			PREVIOUS_BUTTON.setVisible(true);
			title.setText("<html>Question: <font color=\"red\">" + (rdm_index + 1) + "</font> / " + (number - 1) + "</html>");
					
					
			//結束
			if (rdm_index > number - 2) {// 超過資料數就結束  rdm_index長度=9 number=11(以pair 10組 + 1(標題) 為例)
				tim.stop();	
				System.out.println("總共花費:"+time2.getText());
				panel_N.setVisible(true);
				time.setVisible(false);
				time2.setVisible(false);
				time_title.setVisible(false);
				time_title2.setVisible(false);
				PREVIOUS_BUTTON.setVisible(false);
				NEXT_BUTTON.setVisible(false);
				title.setText("完成");				
				panel_q.setVisible(true);				
				vs.setText("<html><body><center><p>請告知相關人員</p><br><p>感謝合作</p><br><center><body></html>");
				question1.setVisible(false);
				question2.setVisible(false);

				
			//下一筆
			} else {// 沒超過，顯示下一筆，時間重計
			
				
				
				/*改變按鈕顏色*/
				if (arr_ans[rdm_index] != null){//有答過的題目
					now_totoalTime_tmp=Integer.parseInt(time2.getText());
					time_cnt=timeArray[rdm_index];
					for(int i = 0; i < label_level; i++) {
						if (i== Integer.parseInt(arr_ans[rdm_index])-1){//-1 -> button從0開始
							buttons[i].setBackground(Color.decode("#3d85c6"));
							buttons[i].setForeground(Color.decode("#cfe2f3"));
						}else{
							buttons[i].setBackground(Color.decode("#cfe2f3"));
							buttons[i].setForeground(Color.decode("#3d85c6"));
						}
					}
				}else{//沒答過
					time_cnt=0;
					backtrack[rdm_index] = false;
					NEXT_BUTTON.setVisible(false);
					for(int i = 0; i < label_level; i++) {
						buttons[i].setBackground(Color.decode("#cfe2f3"));	
						buttons[i].setForeground(Color.decode("#3d85c6"));
					}				
				}
				/*改變按鈕顏色*/
				

				if (rdm_index == Random_Num.length - 1) {//最後一筆
					NEXT_BUTTON.setVisible(false);
				}
			
				//tim.setActionCommand("time");
				question1.setText("<html><body><center>" + x[Random_Num[rdm_index]] + "<center><body></html>");
				question2.setText("<html><body><center>" + y[Random_Num[rdm_index]] + "<center><body></html>");
				
				
			}
			

			//System.out.println(time_cnt);
			/*System.out.print("__題號");
			for(int i=0;i<number-1;i++){
				System.out.print((i+1)+",");
			}System.out.println();
			System.out.print("答題答案");
			for(int i=0;i<number-1;i++){
				System.out.print(arr_ans[i]+",");
			}
			System.out.println();
			System.out.print("時間紀錄");
			for(int i=0;i<number-1;i++){
				System.out.print(timeArray[i]+",");
			}
			System.out.println();
			System.out.print("往回紀錄");
			for(int i=0;i<number-1;i++){
				if (backtrack[i]==true)	System.out.print("T,");
				else System.out.print("F,");
			}
			System.out.println();*/
			
			//System.out.println("下一題rdm_index: "+rdm_index+" ans: "+arr_ans[rdm_index]+" time:"+timeArray[rdm_index]+" back:"+backtrack[rdm_index]);


		}

	}


	public static void main(String[] args) {

		//主畫面的Panel
		main_Panel = new JPanel();
		
		
		//一開始的倒數頁面
		JPanel page_start = new JPanel(new GridBagLayout());
		JL_start = new JLabel("<html><body><center>倒數後進入<br>" + "5" + "<center><body></html>");// 倒數五秒
		Font fnt_start = new Font("Serief", Font.BOLD, 80);
		JL_start.setFont(fnt_start);
		page_start.add(JL_start);// F4FCD9
		page_start.setBackground(Color.decode("#F3F0D7"));
		
		// 設定Timer定時器,並啟動
		tim = new Timer(1000, new labelCount());
		tim.setActionCommand("time_start");// 五秒後開始測驗
		tim.start();
		
		cardLayout = new CardLayout();
		main_Panel.setLayout(cardLayout);
		main_Panel.add("page_start", page_start);//一開始的倒數頁面
		main_Panel.add("dmo", demo);//倒數完的標註畫面

		mainPage.getContentPane().add(main_Panel);
		mainPage.setSize(1500, 800);
		mainPage.setLocation(50,10);
		mainPage.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		mainPage.setVisible(true);

	}
}
