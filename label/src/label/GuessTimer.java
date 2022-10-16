package label;

import javax.swing.JLabel;

import java.util.Timer;

import java.util.TimerTask;

 

/**

 * �p�ɾ��A�i�˼Ƭ����ܡA�åi��ť�O�ɨƥ�

 * @author Ray(java�N�L��)

 *https://blog.xuite.net/ray00000test/blog/66911629

 */

public class GuessTimer{

 public interface Listener{

 //�q���ɶ���

 public void timeOut();

 //����ܰʬ��

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

  * �]�w��ťtimer�ƥ�

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

  * �Ұ�TIMER

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

  * ����TIMER

  * @param s

  */

 public void stopoTimer(){

 if(timer != null){

 timer.cancel();

 timer = null;

 }

 }

 

 public static void main(String [] args){

 

 //�d��

 JLabel lab = new JLabel();

 GuessTimer timer = new GuessTimer();

 timer.setJLabel(lab);

 //��ť�p�ɾ�timeout�ƥ�(�i�諸�ƥ�A����@�]�i�H�ϥ�timer

 timer.addListener(new GuessTimer.Listener() {

 @Override

 public void timeOut() {

 //�B�zTimeOut�ƥ�

 }

 

 @Override

 public void onChange(long sec) {

 System.out.println("sec=>" + sec);

 }

 });

 timer.startTimer(5);

 }

}