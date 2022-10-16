package label;

import javax.swing.JLabel;

import java.util.Timer;

import java.util.TimerTask;

 

/**

 * 計時器，可倒數秒數顯示，並可傾聽逾時事件

 * @author Ray(java吉他手)

 *https://blog.xuite.net/ray00000test/blog/66911629

 */

public class GuessTimer{

 public interface Listener{

 //通知時間到

 public void timeOut();

 //秒數變動秒數

 public void onChange(long sec);

 }

 private Listener lis;

 private Timer timer;

 private JLabel timeLab;

 private long delay;

 private long sec;

 

 public GuessTimer() {

 delay = 1;

 }

 

 public void setJLabel(JLabel lab){

 timeLab = lab;

 }

 

 /**

  * 設定傾聽timer事件

  * @param li

  */

 public void addListener(Listener li){

 lis = li;

 }

 

 public void setJComponent(long d){

 delay = d;

 }

 public void setTime(int s){
	 timer.cancel();
	 timer = null;
	 startTimer(s);
	 //timeLab.setText(String.valueOf(s));
	 

 }

 /**

  * 啟動TIMER

  * @param s

  */

 public void startTimer(int s){
	 timeLab.setText(String.valueOf(s));
	 
	 if(timer == null){
		 
		 timer = new Timer();
		 sec = s;
		
		 TimerTask task = new TimerTask(){
			 
			 public void run(){
			
				 sec -= delay;
				
				 timeLab.setText(String.valueOf(sec));
				
				 if(lis != null){
				
					 lis.onChange(sec);
				
				 }				
				 				
				 if(sec <= 0){			
					 stopoTimer();				
					 if(lis != null){
						 lis.timeOut();				
					 }			
				 }		
			 }
		
		 };

		 long delaySec = delay * 1000;
		 timer.schedule(task, delaySec, delaySec);

	 }

 }

 

 /**

  * 停止TIMER

  * @param s

  */

 public void stopoTimer(){

 if(timer != null){

 timer.cancel();

 timer = null;

 }

 }

 

 public static void main(String [] args){

 

 //範例

 JLabel lab = new JLabel();

 GuessTimer timer = new GuessTimer();

 timer.setJLabel(lab);

 //傾聽計時器timeout事件(可選的事件，不實作也可以使用timer

 timer.addListener(new GuessTimer.Listener() {

 @Override

 public void timeOut() {

 //處理TimeOut事件

 }

 

 @Override

 public void onChange(long sec) {

 System.out.println("sec=>" + sec);

 }

 });

 timer.startTimer(5);

 }

}