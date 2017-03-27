
public class Account {
	private String name;
	private double balance;
	
	public Account(String name, double balance){
		this.name = name;
		
		if(balance > 0.0)
			this.balance = balance;
	}
	
	public void deposit(double depositAmount)
	{
		if (depositAmount > 0.0)
			balance = balance + depositAmount;
	}
	
	public double getBalance()
	{
		return balance;
	}
	
	public void setName(String name)
	{
		this.name = name;
	}
	
	public String getName()
	{
		return name;
	}
	
	public double withdraw(double withdrawAmount)
	{
		if(withdrawAmount<balance){
			balance = balance - withdrawAmount;
		}
		else
			System.out.println("Error: 잔액 부족으로  출금 불가.");
		return balance;
	}
	
	   void setBalance(double amount) 
	   {
	      balance = amount ;
	   }

}
