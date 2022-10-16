package label;

import java.awt.*;
import java.io.*;
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
 * 
 * 倒數版 -> CSV須為11筆  想更改可參考labelCount.java 或 practice.java
 * 
 */
public class countdown implements ActionListener{
    
    static final JFrame demo = new JFrame();
    static final JLabel question1 = new JLabel("Label1",JLabel.CENTER);
    static final JLabel vs = new JLabel("VS",JLabel.CENTER);
    static final JLabel question2 = new JLabel("Label2",JLabel.CENTER);
    static final JLabel title = new JLabel("",JLabel.CENTER);
    static String[] x=null;
    static String[] y=null;
    static int key=1;   
    static JLabel time;
    static GuessTimer timer;    
    static JPanel radioPanel;
    
    public static void main(String[] args) throws FileNotFoundException{

    	//https://www.delftstack.com/zh-tw/howto/java/parse-csv-in-java/
    	String line = "";
        final String delimiter = ",";
        try
        {
            String filePath = "pair10.csv";
            FileReader fileReader = new FileReader(filePath);
            BufferedReader reader = new BufferedReader(fileReader);
            x = new String[11];
            y = new String[11];
            
            int i=0;
            //X跟Y超過四個字就換行
            while ((line = reader.readLine()) != null)   //loops through every line until null found
            {
            	String[] token = line.split(delimiter);    // separate every token by comma
            	//System.out.println(token[0] + " | "+ token[1]);
            	int space_cnt=0;
            	String str_x="";
            	
            	for(int j=0;j<token[0].length();j++) {
            		if(token[0].charAt(j)==32) {
            			space_cnt++;
            			if(space_cnt%4==0) {
            				str_x+="<br>";
            				
            			}else {str_x+=token[0].charAt(j);}
            		}else {str_x+=token[0].charAt(j);}
            	}
            	
            	int space_cnt2=0;
            	String str_y="";
            	for(int j=0;j<token[1].length();j++) {
            		if(token[1].charAt(j)==32) {
            			space_cnt2++;
            			if(space_cnt2 % 4 == 0) {
            				str_y+="<br>";
            				
            			}else {str_y+=token[1].charAt(j);}
            		}else {str_y+=token[1].charAt(j);}
            	}
            	
            	//x[i]=token[0];
            	x[i]=str_x;
            	y[i]=str_y;
            	i++;
            }
            reader.close();
          
        }
        catch (IOException e){e.printStackTrace();}
        
       
        try {
	            File csv = new File("answer.csv");//CSV檔案
			    BufferedWriter bw = new BufferedWriter(new FileWriter(csv, true));
			    //新增一行資料
			    //bw.newLine();
			    bw.write("id" + "," + "ans"+"," +"time");
			    bw.close();
		    } catch (FileNotFoundException e) {
		        //捕獲File物件生成時的異常
		    	e.printStackTrace();
		    } catch (IOException e) {
		        //捕獲BufferedWriter物件關閉時的異常
		    	e.printStackTrace();
		    }
        
        
        demo.setSize(1500, 800);
        demo.setLocation(200,100); 
        demo.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
     
        
        Font fnt2=new Font("Serief",Font.BOLD,50);
        
        
        title.setFont(fnt2);
        title.setText(key+" of 10");
        JPanel panel_N=new JPanel();
        panel_N.setBackground(Color.decode("#96CEB4"));//標題
        panel_N.add(title); 
         
       
        JPanel panel = new JPanel();
        panel.setLayout(new BorderLayout());
        panel.setBackground(Color.green);
        
       
        
        JPanel panel_q = new JPanel();
        panel_q.setLayout(new GridBagLayout());
        GridBagConstraints gbc = new GridBagConstraints();
       
        question1.setText("<html><body><center>"+x[key]+"<center><body></html>");
        question2.setText("<html><body><center>"+y[key]+"<center><body></html>");
        Border blackline = BorderFactory.createLineBorder(Color.black);
        Border margin = new EmptyBorder(30,30,35,30);//上左下右
        question1.setBorder(new CompoundBorder(blackline,margin));
        question2.setBorder(new CompoundBorder(blackline,margin));
       
        question1.setFont(fnt2);   
        vs.setFont(fnt2);
        question2.setFont(fnt2);
        
    
        panel_q.setBackground(Color.decode("#F3F0D7"));//問題板
        
        gbc.weighty = 1;
        
        gbc.gridx = 0;
        gbc.gridy = 0;
        panel_q.add(question1,gbc);
        gbc.gridx = 0;
        gbc.gridy = 1;
        panel_q.add(vs,gbc);
        gbc.gridx = 0;
        gbc.gridy = 2;
        panel_q.add(question2,gbc);
  
        panel.add("Center", panel_q);
        
        time = new JLabel("",JLabel.CENTER);
       
        time.setForeground(Color.red); 
        time.setFont(fnt2);
        JPanel panel_E=new JPanel();
        panel_E.setLayout(new BorderLayout());
        panel_E.setBackground(Color.decode("#F3F0D7"));//時間背景
        panel_E.add(time); 
        
        
        timer = new GuessTimer();
        timer.setJLabel(time);
        timer.startTimer(5);
        
        timer.addListener(new GuessTimer.Listener() {

        	 @Override

        	 public void timeOut() {
        		 System.out.println(key+" timeout");
        		 try {
  		            File csv = new File("answer.csv");//CSV檔案
  				    BufferedWriter bw = new BufferedWriter(new FileWriter(csv, true));
  				    //新增一行資料
  				    bw.newLine();
  				    bw.write(key + ",timeOut,timeOut");
  				    bw.close();
  			    } catch (FileNotFoundException e) {
  			        //捕獲File物件生成時的異常
  			    	e.printStackTrace();
  			    } catch (IOException e) {
  			        //捕獲BufferedWriter物件關閉時的異常
  			    	e.printStackTrace();
  			    }
        		 key++;
        		 title.setText(key+" of 10");
        		 if(key>10) {
        			 	title.setText("Relatedness");
        			 	timer.stopoTimer();
        	    		vs.setText("end");
        	    		time.setVisible(false);
        	    		question1.setVisible(false);
        	    		question2.setVisible(false);
        	    		radioPanel.setVisible(false);
        	    		
        		 }else {       			 
        			 question1.setText("<html><body><center>"+x[key]+"<center><body></html>");
        		     question2.setText("<html><body><center>"+y[key]+"<center><body></html>");
        			 //question.setText("<html><body><center>"+x[key]+"<br><br>"+"VS"+"<br><br>"+y[key]+"<center><body></html>");            		 
            		 timer.startTimer(5);
        		 }
        		 //處理TimeOut事件
        	 }

			@Override
			public void onChange(long sec) {
				// TODO Auto-generated method stub
				
			}
        });
      
  
        
        

        JRadioButton radiobutton = new JRadioButton("JRadiobutton");
        radiobutton.setVisible(false); 
        new countdown();
        
        demo.getContentPane().add(BorderLayout.CENTER ,panel );
        demo.getContentPane().add(BorderLayout.EAST, panel_E);
        demo.getContentPane().add(BorderLayout.NORTH, panel_N);        
        demo.setVisible(true);
	}
    
    public countdown() {
    	
    	
        
    	JRadioButton B1 = new JRadioButton("1");
    	B1.setActionCommand("1");//嚙稽嚙緩嚙踝蕭嚙編嚙踝蕭嚙瞌
    	B1.setSize(350,100);
    	//B1.setSelected(true);
    	JRadioButton B2 = new JRadioButton("2");
        B2.setActionCommand("2");
        JRadioButton B3 = new JRadioButton("3");
        B3.setActionCommand("3");
        JRadioButton B4 = new JRadioButton("4");    
        B4.setActionCommand("4");
        JRadioButton B5 = new JRadioButton("5"); 
        B5.setActionCommand("5");        
    	JRadioButton B6 = new JRadioButton("6");
        B6.setActionCommand("6");
        JRadioButton B7 = new JRadioButton("7");
        B7.setActionCommand("7");
        JRadioButton B8 = new JRadioButton("8");    
        B8.setActionCommand("8");
        JRadioButton B9 = new JRadioButton("9"); 
        B9.setActionCommand("9");
        JRadioButton B10 = new JRadioButton("10"); 
        B10.setActionCommand("10");
        
        B1.setOpaque(false);
        B2.setOpaque(false);
        B3.setOpaque(false);
        B4.setOpaque(false);
        B5.setOpaque(false);
        B6.setOpaque(false);
        B7.setOpaque(false);
        B8.setOpaque(false);
        B9.setOpaque(false);
        B10.setOpaque(false);
        
        Font btn =new Font("Serief",Font.BOLD,50);
        B1.setFont(btn);
        B2.setFont(btn);
        B3.setFont(btn);
        B4.setFont(btn);
        B5.setFont(btn);
        B6.setFont(btn);
        B7.setFont(btn);
        B8.setFont(btn);
        B9.setFont(btn);
        B10.setFont(btn);

        
        //Group the radio buttons.
        ButtonGroup group = new ButtonGroup();        
        group.add(B1);
        group.add(B2);
        group.add(B3);
        group.add(B4);
        group.add(B5);
        group.add(B6);
        group.add(B7);
        group.add(B8);
        group.add(B9);
        group.add(B10);

        //Register a listener for the radio buttons.
        B1.addActionListener(this);
        B2.addActionListener(this);
        B3.addActionListener(this);
        B4.addActionListener(this);
        B5.addActionListener(this);
        B6.addActionListener(this);
        B7.addActionListener(this);
        B8.addActionListener(this);
        B9.addActionListener(this);
        B10.addActionListener(this);
            
        radioPanel = new JPanel(new GridBagLayout());//int rows, int cols
        radioPanel.setBackground(Color.decode("#96CEB4"));
        JLabel high = new JLabel("  High");        
        JLabel low = new JLabel("  Low");
        GridBagConstraints gbc_r = new GridBagConstraints();
        gbc_r.gridx = 0;
        gbc_r.gridy = 0;
        radioPanel.add(low,gbc_r);
        gbc_r.gridx = 9;
        gbc_r.gridy = 0;
        radioPanel.add(high,gbc_r);
        Font fnt3=new Font("Serief",Font.BOLD,20);
        high.setFont(fnt3);
        low.setFont(fnt3);
        
        gbc_r.weightx = 1;
        gbc_r.gridx = 0;
        gbc_r.gridy = 1;
        radioPanel.add(B1,gbc_r);
        gbc_r.gridx = 1;
        gbc_r.gridy = 1;
        radioPanel.add(B2,gbc_r);
        gbc_r.gridx = 2;
        gbc_r.gridy = 1;
        radioPanel.add(B3,gbc_r);
        gbc_r.gridx = 3;
        gbc_r.gridy = 1;
        radioPanel.add(B4,gbc_r);
        gbc_r.gridx = 4;
        gbc_r.gridy = 1;
        radioPanel.add(B5,gbc_r);
        gbc_r.gridx = 5;
        gbc_r.gridy = 1;
        radioPanel.add(B6,gbc_r);
        gbc_r.gridx = 6;
        gbc_r.gridy = 1;
        radioPanel.add(B7,gbc_r);
        gbc_r.gridx = 7;
        gbc_r.gridy = 1;
        radioPanel.add(B8,gbc_r);
        gbc_r.gridx = 8;
        gbc_r.gridy = 1;
        radioPanel.add(B9,gbc_r);
        gbc_r.gridx = 9;
        gbc_r.gridy = 1;
        radioPanel.add(B10,gbc_r);
        


        
        demo.add(BorderLayout.SOUTH,radioPanel);
        
    }
     
    public void actionPerformed(ActionEvent e) {
    	String cmd = e.getActionCommand();

		System.out.println(key+" "+cmd);
		
    	try {
            File csv = new File("answer.csv");//CSV檔案
		    BufferedWriter bw = new BufferedWriter(new FileWriter(csv, true));
		    //新增一行資料
		    bw.newLine();
		    bw.write(key + "," + cmd + "," + time.getText());
		    bw.close();
	    } catch (FileNotFoundException e1) {
	        //捕獲File物件生成時的異常
	    	e1.printStackTrace();
	    } catch (IOException e1) {
	        //捕獲BufferedWriter物件關閉時的異常
	    	e1.printStackTrace();
		}
    	key++;
    	title.setText(key+" of 10");
    	if(key>10) {
    		title.setText("Relatedness");
    		timer.stopoTimer();
			vs.setText("end");
			question1.setVisible(false);
			question2.setVisible(false);
			//question.setVisible(true);
			time.setVisible(false);
			radioPanel.setVisible(false);
		}else {
	    	question1.setVisible(false);
	    	question2.setVisible(false);
	    	//timer.stopoTimer();
	    	timer.setTime(5);
	    	question1.setText("<html><body><center>"+x[key]+"<center><body></html>");
	        question2.setText("<html><body><center>"+y[key]+"<center><body></html>");
	    	//question.setText("<html><body><center>"+x[key]+"<br><br>"+"VS"+"<br><br>"+y[key]+"<center><body></html>");
	    	question1.setVisible(true);
	    	question2.setVisible(true);
		}
    }


}

