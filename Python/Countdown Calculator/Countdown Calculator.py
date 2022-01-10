numbers = [50, 75, 1, 6, 2, 8]
target = 360
answer = False
win = "dont"
operations = ['+', '-', '*', '/']

def getAns(ops, inputNums, num1=0, num2=0, num3=0, num4=0, num5=0, num6=0):
    numVars = [num1, num2, num3, num4, num5, num6]
    nums = [i for i in inputNums]
    for i in range(6 - len(inputNums)):
        nums.append(numVars[-i])

    num1 = nums[0]
    num2 = nums[1]
    num3 = nums[2]
    num4 = nums[3]
    num5 = nums[4]
    num6 = nums[5]
    
    for i in range(len(ops)):
        nums = [num1, num2, num3, num4, num5, num6]
        op = ops[i]
        if op == '+':
            nums[i+1] = nums[i] + nums[i+1]
        elif op == '-':
            nums[i+1] = nums[i] - nums[i+1]
        elif op == '*':
            nums[i+1] = nums[i] * nums[i+1]
        elif op == '/':
            nums[i+1] = nums[i] / nums[i+1]
        ans = nums[i+1]
    #print(ans)
    return ans



for op1 in operations:
    #if answer:
       # break
    
    for op2 in operations:
        #if answer:
          #  break
        
        for op3 in operations:
            #if answer:
                #break
            
            for op4 in operations:
                #if answer:
                    #break
                #print("here")

                for op5 in operations:
                
                    for num1 in numbers:
                        #if answer:
                           # break
                        
                        for num2 in numbers:
                            if num2 != num1:
                                #if answer:
                                   # break
                                ops = [op1]
                                nums = [num1, num2]
                                answer = (getAns(ops, nums))
                                if answer == target:
                                    win = ("Got it")
                                    break
                                
                                for num3 in numbers:
                                    if num3 != num2 and num3 != num1:
                                        #if answer:
                                            #break
                                        ops = [op1, op2]
                                        nums = [num1, num2, num3]
                                        answer = (getAns(ops, nums))
                                        if answer == target:
                                            win = ("Got it")
                                            break
                                    
                                        for num4 in numbers:
                                            if num4 != num3 and num4 != num2 and num4 != num1:
                                                #if answer:
                                                    #break
                                                ops = [op1, op2, op3]
                                                nums = [num1, num2, num3, num4]
                                                answer = (getAns(ops, nums))
                                                if answer == target:
                                                    win = ("Got it")
                                                    break

                                                for num5 in numbers:
                                                    if num5 != num4 and num5 != num3 and num5 != num2 and num5 != num1:                                                        

                                                        op1 = '+'
                                                        op2 = '*'
                                                        op3 = '+'
                                                        op4 = '+'
                                                        num1 = 6
                                                        num2 = 1
                                                        num3 = 50
                                                        num4 = 2
                                                        num5 = 8
                                                        
                                                        ops = [op1, op2, op3, op4]
                                                        nums = [num1, num2, num3, num4, num5]
                                                        answer = (getAns(ops, nums))

                                                        if answer == target:
                                                            win = ("Got it")
                                                            break
                                            
                                                        for num6 in numbers:
                                                            if num6 != num5 and num6 != num4 and num6 != num3 and num6 != num2 and num6 != num1:

                                                                ops = [op1, op2, op3, op4, op5]
                                                                nums = [num1, num2, num3, num4, num5, num6]
                                                                answer = (getAns(ops, nums))
                                                                
                                                                #print(answer)
                                                                if answer == target:
                                                                    #answer = True
                                                                    win = ("Got it")
                                                                    break
print(win)
print("done")

#num1, op1, num2, op2, num3, op3, num4, op4, num5, op5, num6

