//
//  UIViewController+SearchCreditAssetViewController.m
//  Loan_UI
//
//  Created by MillionBenjamin on 2019/12/13.
//  Copyright © 2019 中山大学. All rights reserved.
//

#import "SearchCreditAssetViewController.h"
#import "AppDelegate.h"
#import "Masonry.h"
#import "AFNetworking.h"
#import "NoResultViewController.h"
#import "CreditAssetResultViewController.h"

@interface SearchCreditAssetViewController ()

@end

@implementation SearchCreditAssetViewController

- (void)viewWillAppear:(BOOL)animated {
    [super viewWillAppear:YES];
    [self.view addSubview:self.bNameInputField];
    [self.view addSubview:self.cpNameInputField];
    /*
    UIEdgeInsets inset_input = UIEdgeInsetsMake(230, 100, 600, 100);
    
    [self.guideLabel mas_makeConstraints:^(MASConstraintMaker *make){
        make.edges.equalTo(self.view).with.insets(inset_input);
    }];
     */

}


- (void)viewDidLoad {
    [super viewDidLoad];
    
    [self.view addSubview: self.guideLabel];
    //inset distance to (top, left, bottom, right)
    UIEdgeInsets inset_title = UIEdgeInsetsMake(200, 50, 600, 50);
    [self.guideLabel mas_makeConstraints:^(MASConstraintMaker *make){
        make.edges.equalTo(self.view).with.insets(inset_title);
    }];
    
    [self.view addSubview: self.confirmButton];
    

}


- (UILabel *)guideLabel {
    if(_guideLabel == nil) {
        _guideLabel = [[UILabel alloc] init];
        [_guideLabel setText: @"请输入银行名称和公司名称"];
        [_guideLabel setFont: [UIFont systemFontOfSize: 23]];
        [_guideLabel setTextColor: [UIColor blackColor]];
        [_guideLabel setTextAlignment:NSTextAlignmentCenter];
        //_guideLabel.backgroundColor = [UIColor blueColor];
    }
    return _guideLabel;
}


- (UITextField *)bNameInputField {
    if(_bNameInputField == nil) {
        NSInteger fieldWidth = 275;
        _bNameInputField = [[UITextField alloc]initWithFrame:CGRectMake(self.view.frame.size.width / 2 - fieldWidth / 2, 300, fieldWidth, 40)];
        _bNameInputField.borderStyle = UITextBorderStyleRoundedRect;
        _bNameInputField.backgroundColor = [UIColor whiteColor];
        _bNameInputField.placeholder = @"银行名称";
        _bNameInputField.font = [UIFont systemFontOfSize:20];
        _bNameInputField.clearButtonMode = UITextFieldViewModeAlways;
        _bNameInputField.autocapitalizationType = UITextAutocapitalizationTypeNone;
        //_bNameInputField.textAlignment = NSTextAlignmentCenter;
    }
    return _bNameInputField;
}


- (UITextField *)cpNameInputField {
    if(_cpNameInputField == nil) {
        NSInteger fieldWidth = 275;
        _cpNameInputField = [[UITextField alloc]initWithFrame:CGRectMake(self.view.frame.size.width / 2 - fieldWidth / 2, 380, fieldWidth, 40)];
        _cpNameInputField.borderStyle = UITextBorderStyleRoundedRect;
        _cpNameInputField.backgroundColor = [UIColor whiteColor];
        _cpNameInputField.placeholder = @"公司名称";
        _cpNameInputField.font = [UIFont systemFontOfSize:20];
        _cpNameInputField.clearButtonMode = UITextFieldViewModeAlways;
        _cpNameInputField.autocapitalizationType = UITextAutocapitalizationTypeNone;
        //_cpNameInputField.textAlignment = NSTextAlignmentCenter;
    }
    return _cpNameInputField;
}



- (UIButton*)confirmButton {
    if (_confirmButton == nil) {
        
        _confirmButton = [UIButton buttonWithType:UIButtonTypeRoundedRect];
        _confirmButton.clipsToBounds = YES;
        [_confirmButton.layer setCornerRadius:10.0];
        [_confirmButton.layer setMasksToBounds:YES];
        
        NSUInteger buttonWidth = 160;
        _confirmButton.frame = CGRectMake(self.view.frame.size.width / 2 - buttonWidth / 2, 460, buttonWidth, 50);
        
        [_confirmButton setBackgroundColor:[UIColor systemBlueColor]];
        [_confirmButton.layer setBorderColor:[UIColor clearColor].CGColor];
        [_confirmButton setTitleColor:[UIColor whiteColor] forState:0];
        
        _confirmButton.titleLabel.font = [UIFont systemFontOfSize:20];
        [_confirmButton setTitle:@"查询" forState:0];
        
        [_confirmButton addTarget:self action:@selector(confirmButtonClick:) forControlEvents:UIControlEventTouchUpInside];
        
        _confirmButton.userInteractionEnabled = YES;
    }
    return _confirmButton;
}


- (void) confirmButtonClick:(id)sender {
    NSURLSessionConfiguration *defaultConfigObject = [NSURLSessionConfiguration defaultSessionConfiguration];
    NSURLSession *delegateFreeSession = [NSURLSession sessionWithConfiguration: defaultConfigObject
                                                                          delegate: self
                                                                     delegateQueue: [NSOperationQueue mainQueue]];
    NSURL *url = [NSURL URLWithString:[NSString stringWithFormat: @"http://172.16.207.150:8383/get_AmountOfCreditAsset_bank_GiveTo_TrustedCompany/?bName=%@&cpName=%@",self.bNameInputField.text, self.cpNameInputField.text]];
    NSURLRequest *request = [NSURLRequest requestWithURL:url];

    NSURLSessionDataTask * dataTask = [delegateFreeSession dataTaskWithRequest:request
        completionHandler:^(NSData *data, NSURLResponse *response, NSError *error) {
        if(error == nil) {
            NSString * text = [[NSString alloc] initWithData: data encoding: NSUTF8StringEncoding];
            NSData* jsonData = [text dataUsingEncoding:NSUTF8StringEncoding];
            NSDictionary* dic = [NSJSONSerialization JSONObjectWithData:jsonData options:NSJSONReadingAllowFragments error:&error];
            NSLog(@"%@", dic);
            if(dic[@"amount"] != nil) {
                AppDelegate *myDelegate = (AppDelegate*)[[UIApplication sharedApplication]delegate];
                CreditAssetResultViewController* qc = [[CreditAssetResultViewController alloc] init];
                qc.title = @"查询结果";
                
                [qc.participantLabel setText:[NSString stringWithFormat:@"银行%@向公司%@", self.bNameInputField.text, self.cpNameInputField.text]];
                [qc.amountLabel setText:[NSString stringWithFormat:@"授权信用资产数额：%@", dic[@"amount"]]];
            
                
            
                [myDelegate.nc pushViewController:qc animated:YES];
            }
            else {
                AppDelegate *myDelegate = (AppDelegate*)[[UIApplication sharedApplication]delegate];
                NoResultViewController* qc = [[NoResultViewController alloc] init];
                [myDelegate.nc pushViewController:qc animated:YES];
            }
            /*
            for(int i = 0; i < self->mainCollectionView.numberOfSections; i++) {
                QuestionCollectionViewCell *cell = (QuestionCollectionViewCell *)[self->mainCollectionView cellForItemAtIndexPath:[NSIndexPath indexPathForRow:0 inSection:i]];
                        
                [cell.QuestionButton setTitle:dic[@"data"][self->currentPage][@"choices"][i] forState:0];
            }
            self.QuestionLabel.text = dic[@"data"][self->currentPage][@"question"];
             */
        }
        }];
            
        [dataTask resume];
    

}




@end
